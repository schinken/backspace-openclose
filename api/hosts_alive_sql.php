<?php

$hostQueries = array(
   'all' => "SELECT COUNT(*) as count FROM alive_hosts WHERE erfda = (SELECT erfda FROM alive_hosts WHERE erfda > NOW() - INTERVAL 6 MINUTE ORDER by erfda DESC LIMIT 1)",
   'members' => "SELECT COUNT(*) as count FROM ( SELECT 1 FROM alive_hosts AS t1 INNER JOIN mac_to_nick AS t2 ON t1.macaddr = t2.macaddr AND t2.privacy < 3 WHERE erfda = (SELECT erfda FROM alive_hosts WHERE erfda > NOW() - INTERVAL 6 MINUTE ORDER by erfda DESC LIMIT 1) GROUP by nickname) as ghoti",
   'member_devices' => "SELECT COUNT(*) as count FROM alive_hosts as t1 INNER JOIN mac_to_nick as t2 ON t1.macaddr = t2.macaddr AND t2.privacy < 3 WHERE erfda = (SELECT erfda FROM alive_hosts WHERE erfda > NOW() - INTERVAL 6 MINUTE ORDER by erfda DESC LIMIT 1)",
   'unknown' => "SELECT COUNT(*) as count FROM alive_hosts as t1 LEFT OUTER JOIN mac_to_nick as t2 ON t1.macaddr = t2.macaddr AND t2.privacy < 3 WHERE t2.macaddr IS NULL AND erfda = (SELECT erfda FROM alive_hosts WHERE erfda > NOW() - INTERVAL 6 MINUTE ORDER by erfda DESC LIMIT 1)"
);

?>
