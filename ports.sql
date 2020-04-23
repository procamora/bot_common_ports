BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Ports";
CREATE TABLE IF NOT EXISTS "Ports" (
    "name"  TEXT NOT NULL,
    "port"  INTEGER NOT NULL,
    "protocol"  TEXT NOT NULL,
    "description"   TEXT,
    PRIMARY KEY("port")
);

DROP TABLE IF EXISTS "Stats";
CREATE TABLE IF NOT EXISTS "Stats" (
    "id"            INTEGER NOT NULL,
    "id_user"       INTEGER NOT NULL,
    "id_port"       INTEGER NOT NULL,
    "successful"    TEXT NOT NULL,
    PRIMARY KEY("id")
);



INSERT INTO "Ports" VALUES ('fttp-data',20,'tcp','File Transfer Protocol (FTP) data transfer');
INSERT INTO "Ports" VALUES ('ftp',21,'tcp','File Transfer Protocol (FTP) control (command)');
INSERT INTO "Ports" VALUES ('ssh',22,'tcp','Secure Shell (SSH),secure logins, file transfers (scp, sftp) and port forwarding');
INSERT INTO "Ports" VALUES ('telnet',23,'tcp','Telnet protocol—unencrypted text communications');
INSERT INTO "Ports" VALUES ('SMTP',25,'tcp','Simple Mail Transfer Protocol (SMTP), used for email routing between mail servers');
INSERT INTO "Ports" VALUES ('domain',53,'both','Domain Name Server (DNS)');
INSERT INTO "Ports" VALUES ('bootps',67,'udp','Server Dynamic Host Configuration Protocol (DHCP)');
INSERT INTO "Ports" VALUES ('bootpc',68,'udp','Client Dynamic Host Configuration Protocol (DHCP)');
INSERT INTO "Ports" VALUES ('tftp',69,'udp','Trivial File Transfer Protocol (TFTP)');
INSERT INTO "Ports" VALUES ('www-http',80,'tcp','Hypertext Transfer Protocol (HTTP)');
INSERT INTO "Ports" VALUES ('Kerberos',88,'udp','Kerberos authentication system');

INSERT INTO "Ports" VALUES ('pop3',110,'tcp','Post Office Protocol, version 3 (POP3)');
INSERT INTO "Ports" VALUES ('sftp',115,'tcp','Simple File Transfer Protocol');
INSERT INTO "Ports" VALUES ('ntp',123,'udp','Network Time Protocol (NTP), used for time synchronization');
INSERT INTO "Ports" VALUES ('netbios-ns',137,'both','NetBIOS Name Service, used for name registration and resolution');
INSERT INTO "Ports" VALUES ('netbios-dgm',138,'udp','NetBIOS Datagram Service');
INSERT INTO "Ports" VALUES ('netbios-ssn',139,'tcp','NetBIOS Session Service');
INSERT INTO "Ports" VALUES ('imap',143,'tcp','Internet Message Access Protocol (IMAP),management of electronic mail messages on a server');
INSERT INTO "Ports" VALUES ('snmp',161,'udp','Simple Network Management Protocol (SNMP)');
INSERT INTO "Ports" VALUES ('snmp-trap',162,'both','Simple Network Management Protocol Trap (SNMPTRAP)');
INSERT INTO "Ports" VALUES ('irc',194,'both','Internet Relay Chat (IRC)');

INSERT INTO "Ports" VALUES ('imap3',220,'both','Internet Message Access Protocol (IMAP), version 3');

INSERT INTO "Ports" VALUES ('ldap',389,'tcp','Lightweight Directory Access Protocol (LDAP)');

INSERT INTO "Ports" VALUES ('https',443,'tcp','Hypertext Transfer Protocol over TLS/SSL (HTTPS)');
INSERT INTO "Ports" VALUES ('microsoft-ds',445,'both','Microsoft-DS (Directory Services) Active Directory, SMB file sharing');
-- INSERT INTO "Ports" VALUES ('smtps',465,'tcp','Authenticated SMTP over TLS/SSL (SMTPS)');

INSERT INTO "Ports" VALUES ('ike',500,'udp','Internet Security Association and Key Management Protocol (ISAKMP)/Internet Key Exchange (IKE)');

INSERT INTO "Ports" VALUES ('ldaps',636,'tcp','LDAP over SSL');

INSERT INTO "Ports" VALUES ('dns-s',853,'both','DNS over TLS');
INSERT INTO "Ports" VALUES ('rsync',873,'tcp','rsync file synchronization protocol');

INSERT INTO "Ports" VALUES ('ftps-data',989,'both','FTPS Protocol (data), FTP over TLS/SSL');
INSERT INTO "Ports" VALUES ('ftps',990,'both','FTPS Protocol (control), FTP over TLS/SSL');
INSERT INTO "Ports" VALUES ('telnets',992,'both','Telnet protocol over TLS/SSL');
INSERT INTO "Ports" VALUES ('imaps',993,'tcp','Internet Message Access Protocol over TLS/SSL (IMAPS)');
INSERT INTO "Ports" VALUES ('pop3s',995,'both','Post Office Protocol 3 over TLS/SSL (POP3S)');

INSERT INTO "Ports" VALUES ('openvpn',1194,'both','OpenVPN');

INSERT INTO "Ports" VALUES ('l2tp',1701,'both','Layer 2 Forwarding Protocol (L2F)');
INSERT INTO "Ports" VALUES ('pptp',1723,'tcp','Point-to-Point Tunneling Protocol (PPTP)');

INSERT INTO "Ports" VALUES ('radius',1812,'both','RADIUS authentication protocol, radius');
INSERT INTO "Ports" VALUES ('radius-acct',1813,'both','RADIUS accounting protocol, radius-acct');

INSERT INTO "Ports" VALUES ('nfs',2049,'both','Network File System (NFS)');

INSERT INTO "Ports" VALUES ('mysql',3306,'tcp','MySQL database system');
INSERT INTO "Ports" VALUES ('rdp',3389,'both','RDP (Remote Desktop Protocol) Terminal Server');

INSERT INTO "Ports" VALUES ('ipsec-nat-t',4500,'udp','IPSec NAT Traversal');

INSERT INTO "Ports" VALUES ('sip',5060,'both','Session Initiation Protocol (SIP)');
INSERT INTO "Ports" VALUES ('sip',5061,'both','Session Initiation Protocol (SIP) over TLS');





COMMIT;
