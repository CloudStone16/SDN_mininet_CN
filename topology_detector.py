from ryu.base import app_manager
from ryu.controller.handler import set_ev_cls
from ryu.topology.event import (
    EventSwitchEnter,
    EventSwitchLeave,
    EventLinkAdd,
    EventLinkDelete
)
import logging

class TopologyDetector(app_manager.RyuApp):
    """
    Topology Change Detector
    Detects changes in network topology dynamically.
    Responsibilities:
    - Monitor switch/link events
    - Update topology map
    - Display changes
    - Log updates
    """
    
    def __init__(self, *args, **kwargs):
        super(TopologyDetector, self).__init__(*args, **kwargs)
        self.switches = set()
        self.links = set()
        self.logger.setLevel(logging.INFO)
        self.logger.info("Topology Change Detector Started...")
        self.logger.info("Monitoring switch and link events...")

    @set_ev_cls(EventSwitchEnter)
    def switch_enter_handler(self, ev):
        switch = ev.switch
        if switch.dp.id not in self.switches:
            self.switches.add(switch.dp.id)
            self._log_change("Switch Connected", f"Switch DPID: {switch.dp.id}")

    @set_ev_cls(EventSwitchLeave)
    def switch_leave_handler(self, ev):
        switch = ev.switch
        if switch.dp.id in self.switches:
            self.switches.remove(switch.dp.id)
            # Remove associated links when a switch leaves to keep map accurate
            links_to_remove = [link for link in self.links if link[0] == switch.dp.id or link[2] == switch.dp.id]
            for link in links_to_remove:
                self.links.remove(link)
            self._log_change("Switch Disconnected", f"Switch DPID: {switch.dp.id}")

    @set_ev_cls(EventLinkAdd)
    def link_add_handler(self, ev):
        link = ev.link
        src_dpid = link.src.dpid
        dst_dpid = link.dst.dpid
        src_port = link.src.port_no
        dst_port = link.dst.port_no
        
        link_id = (src_dpid, src_port, dst_dpid, dst_port)
        if link_id not in self.links:
            self.links.add(link_id)
            self._log_change(
                "Link Added", 
                f"Switch {src_dpid} (Port {src_port}) <----> Switch {dst_dpid} (Port {dst_port})"
            )

    @set_ev_cls(EventLinkDelete)
    def link_delete_handler(self, ev):
        link = ev.link
        src_dpid = link.src.dpid
        dst_dpid = link.dst.dpid
        src_port = link.src.port_no
        dst_port = link.dst.port_no
        
        link_id = (src_dpid, src_port, dst_dpid, dst_port)
        if link_id in self.links:
            self.links.remove(link_id)
            self._log_change(
                "Link Deleted", 
                f"Switch {src_dpid} (Port {src_port}) <X X> Switch {dst_dpid} (Port {dst_port})"
            )
            
    def _log_change(self, event_type, details):
        """Logs the update and displays the new topology map."""
        self.logger.info(f"*** TOPOLOGY CHANGE DETECTED: {event_type} ***")
        self.logger.info(f"Details: {details}")
        self._update_and_display_topology_map()
        
    def _update_and_display_topology_map(self):
        """Updates internal state representations and displays the map."""
        self.logger.info("\n=== Current Topology Map ===")
        self.logger.info(f"Active Switches: {sorted(list(self.switches))}")
        self.logger.info("Active Links:")
        if not self.links:
            self.logger.info("  None")
        for link in sorted(list(self.links)):
            self.logger.info(f"  Switch {link[0]} (port {link[1]}) -> Switch {link[2]} (port {link[3]})")
        self.logger.info("============================\n")
