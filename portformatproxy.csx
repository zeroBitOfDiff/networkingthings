using static System.Console;
using static CANAPE.CLI.ConsoleUtils;

//Create proxy template
var template = new FixedProxyTemplate();
template.LocalPort = LOCALPORT;
template.Host = "REMOTEHOST";
template.Port = REMOTEPORT;

// Create proxy instance and start 
var service = template.Create();
service.Start();

WriteLine("Created {0}", service);
WriteLine("Press Enter to exit...");
ReadLine();
service.Stop();

// Dump packets
var packets = service.Packets;
WriteLine("Captured {0} packets:", packets.Count);
WritePackets(packets);