# wick3d-cl0ne
A wireless penetration testing tool: Clone an access point in **Kali Linux**.

ewicked-cl0ne.py clones an access point with the same SSID and security settings as a target access point OR spawns a fake access point with its own network and security configurations. Dependencies are installed prior to starting. The configuration files (hostapd.conf) and (dnsmasq.conf) are created with pre-populated and pre-defined network and security parameters. These configuration files are automatically installed in a new folder called "/evil-twin," in the current path. Users are prompted to enter a few network parameters prior to starting the access point, but can modify the configuration files as they see fit. Iptables and IP forwarding are configured automatically to forward network traffic on behalf of wireless clients connected to the access point.

**NOTE:** evil-twin.py requires a wireless network adapter. Some knowledge of hostapd and dnsmasq is also beneficial.

# Dependencies:
`pip3 install -r requirements.txt`

# Installation:
`git clone https://github.com/dcfitz11/wick3d-cl0ne.git`

## wick3d-cl0ne checks for the following dependences and installs, if necessary:

**Aircrack-ng**  
A network software suite consisting of a detector, packet sniffer, WEP, and WPA/WPA2-PSK cracker and analysis tool for 802.11 wireless LANs. (Note: There is no requirement for Aircrack-ng at the moment, but future add-ons may require it.

**Hostapd**  
A program (or daemon) primarily used to create wireless access points that follow IEEE 802.11 and its various authentication mechanisms, including WPA2-PSK and 802.1X encryption. Settings are stored in evil-twin/hostapd.conf. <b>NOTE: hostapd will deauth all users from the real access point in order for legitimate clients to access the fake access point</b>

**Dnsmasq**  
A lightweight, easy to configure DNS forwarder, designed to provide DNS (and optionally DHCP and TFTP) services to a small-scale network. Clients that authenticate to the fake access point are provided Internet access via dnsmasq. Settings are stored in evil-twin.hostapd.conf


# Uses:
Install a soft access point on your network to test intrusion detection and prevention security controls, Wi-Fi analysis tools, other wireless security tools, and users' Wi-Fi security awareness. Or simply create a soft access point in a penetration testing engagement.

# Features:
## Users can specify numerous network and security customizations, some of which are already pre-defined in the hostapd and dnsmasq configuration files:

<ul>
 <li>Spawn your own access point. Give it whatever network name and passphrase you wish.</li>
 <li>Clone an existing access point (If not open authentication, you should know the passphrase for the access point you wish to clone).</li>
 <li>Select from various ieee 802.11 wireless technologies (802.11b/g/n).</li>
 <li>Choose your own channel to broadcast your fake access point.</li>
 <li>Choose your authentication type (e.g., WPA-PSK).</li>
 <li>Choose your encryption type (e.g., CCMP, AES).</li>
 <li>Create an Open access point (no authentication).</li>
 <li>Enable dhcp settings to lease clients IP addresses.</li>
 <li>Specify your own dhcp range for your fake access point.</li>
 <li>Log dhcp information to see all dhcp bindings as they occur.</li>
 <li>Choose which public dns servers to use for domain-name resolving and Internet access.</li>
 <li>Log dns queries to see what clients are making dns queries to out on the Internet.</li>
 <li>IP forwarding and automatic iptables modification for Network Address Translation.</li>
 <li>Cleanup functions that restore all network settings and iptables chains upon exit or interruption.</li> 
</ul>

# Helpful Information:
The configuration files <i>contain brackets [ ]</i>. At least these areas should be modified in the configuration files and saved prior to starting the access point. Do **NOT** include the brackets "[]" inside the configuration files. The remaining parameters are default parameters that provide the remaining functionality, but they can be changed according to user preference. See hostapd and dnsmasq man pages and configuration files for more information.

## Modifying the hostapd.conf file:
The hostapd.conf file is pre-populated with the following parameters, by default:
<ul>
 <li><b>interface=[INTERFACE NAME]"</b> // hostapd will start the fake AP on this wireless interface.</li> 
 <li><b>"driver=nl80211"</b> // By default, this is 802.11 netlink interface public interface, used with all Linux mac80211 drivers.</li> 
 <li><b>"ssid=[CLONED NETWORK NAME]"</b> // The name of the wireless network to spawn or clone.</li>
 <li><b>"hw_mode=g"</b> // The wireless operating mode technology (e.g., 802.11a/b/g/n. 802/11g is capable of both 2.4/5GHz frequency ranges.</li> 
 <li><b>"channel=[CHANNEL#]"</b> // The channel you wish to clone the fake access point (e.g., 1, 6, or 11).</li>
 <li><b>"macaddr_acl=0"</b> // MAC address-based authentication using an ACL. "0" accepts all MAC addresses.</li> 
 <li><b>"ignore_broadcast_ssid=0"</b> // Disables the 'ignore broadcast ssid' feature.</li> 
 <li><b>"auth_algs=1"</b> // Defines the authentication algorithm to use. "0" for Open authentication.</li>
 <li><b>"wpa=2"</b> // Sets WPA2 by default, since most Wi-Fi networks are not utilizing WEP or WPA any longer.</li> 
 <li><b>"wpa_passphrase=[NETWORK PASSPHRASE]"</b> // Enter the passphrase for your face access point.</li>
 <li><b>"wpa_key_mgmt=WPA-PSK"</b> // Set to WPA Pre-Shared Key (PSK) authentication, popular on most home Wi-Fi networks.</li> 
 <li><b>"wpa_pairwise=CCMP"</b> // Sets the encryption mechanism to CCMP-AES, as it should on all WPA2 networks.</li> 
 <li><b>"wpa_group_rekey=86400"</b>  // This is the re-keying period in seconds for the Group Temporal Key (GTK).</li>
 <li><b>"ieee80211n=1"</b>  // Enables 802.11m wireless support.</li>
 <li><b>"wme_enabled=1"</b> // Enables Wireless Multimedia Extension (WME) support, by default.</li> 
</ul>

## Modifying the dnsmasq.conf file:
The dnsmasq.conf file is pre-populated with the following parameters, by default:

<ul>
 <li><b>"interface=[INTERFACE NAME]"</b>  // dnsmasq will listen on this wireless interface.</li>   
 <li><b>"dhcp-range=[1st HOST IP ADDRESS,LAST HOST IP ADDRESS,SUBNETMASK,LEASE HOURS]"</b>  // the dhcp leasing range, subnet mask, and dhcp binging leasing time.</li>  
 <li><b>"dhcp-option= 3,[GATEWAY IP ADDRESS]"</b> // Option 3 specifies the gateway IP address.</li>  
 <li><b>"dhcp-option=6,[GATEWAY IP ADDRESS]"</b> // Option 6 configures dhcp clients to use the dns servers in this file (see below).</li> 
 <li><b>"server=8.8.8.8"</b> // Added Google's public DNS servers, but add whichever dns servers you wish.</li> 
 <li><b>"server=8.8.4.4"</b> // Added Google's public DNS servers,  but add whichever dns servers you wish.</li>  
 <li><b>"log-queries"</b>  // Logs what DHCP clients are making DNS queries to.</li> 
 <li><b>"log-dhcp"</b> // Log current DHCP bindings.</li> 
 <li><b>"listen-address=127.0.0.1"</b> // Loopback address.</li>  
</ul>
