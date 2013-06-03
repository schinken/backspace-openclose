from collector import ubiquiti, arp, nmap
import settings

if __name__ == '__main__':
    
    collectors = []
    net = '10.1.20.100-250'

    # ====== add ubuquiti ======
    ubnt = settings.ubiquiti

    x = ubiquiti.Collector(net, ubnt['host'], ubnt['user'], ubnt['pass'])
    x.start()

    collectors.append(x)

    # ====== add arp =======
    x = arp.Collector(net)
    x.start()

    collectors.append(x)

    # ====== add nmap ======
    x = nmap.Collector(net)
    x.start()

    collectors.append(x)


    # waiting for collectors...
    for collector in collectors:
        collector.join()

    # results
    print "The results are in!"

    hosts = {}
    for collector in collectors:
        hosts = dict(hosts.items() + collector.get_hosts().items())

    print hosts




    
