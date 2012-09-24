<?php

include('hosts_alive_sql.php');

$usage = "Use: " . $_SERVER['PHP_SELF'] . "?response=[json|xml|img|ascii]";

if (!$_GET['response'])
	exit($usage);
else
	$get = $_GET['response'];

$db_host = 'localhost';
$db = 'database';
$db_user = 'dbuser';
$db_pass = 'dbpass';

$con = mysql_connect($db_host, $db_user, $db_pass) 
	or die(mysql_error());

function get_hosts_alive($con, $query, $db){

        mysql_select_db($db);
	$result = mysql_query($query, $con);
	$count = mysql_fetch_array($result);

	return $count['count'];
	
}

$hosts = array(	
		'all' => (int) get_hosts_alive($con, $hostQueries['all'], $db),
		'members' => (int) get_hosts_alive($con, $hostQueries['members'], $db),
		'member_devices' => (int) get_hosts_alive($con, $hostQueries['member_devices'], $db),
		'unknown_devices' => (int) get_hosts_alive($con, $hostQueries['unknown'], $db)
	      );

$usr_qry = "select nickname FROM ( SELECT nickname from alive_hosts as t1 INNER JOIN mac_to_nick as t2 ON t1.macaddr = t2.macaddr AND t2.privacy = 0 WHERE erfda > NOW() - INTERVAL 20 MINUTE GROUP by nickname) as ghoti";
$result = mysql_query($usr_qry, $con);

$users = array();
while( $f = mysql_fetch_assoc($result) ) {
    $users[] = array(
        'nickname'  => $f['nickname'] 
    );
}


switch($get){
	case "img":
		if( $hosts['all'] > 0 )
			$img = 'img/status_open.png';
		else
			$img = 'img/status_closed.png';

		$fp = fopen($img, 'r');
		header("Content-Type: image/png");
		header("Content-Length: " . filesize($img));
		fpassthru($fp);
		break;

	case "json":
		header('Content-type: application/json');
        $hosts['members_present'] = $users;
		echo json_encode($hosts);
		break;

	case "ascii":
		header('Content-type: text/html');
		echo "members: " . $hosts['members'];
		break;

	case "xml":
		header("Content-type: text/xml");
		echo '<?xml version="1.0" encoding="utf-8" ?>';
		echo '<xmlresponse>';
		echo '<alive_hosts>' . $hosts['all'] . '</alive_hosts>';
		echo '<members>' . $hosts['members'] . '</members>';
		echo '<member_devices>' . $hosts['member_devices'] . '</member_devices>';
		echo '<unknown_devices>' . $hosts['unknown_devices'] . '</unknown_devices>';
        echo '<members_present>';
        foreach( $users as $user ) {
            echo '<member>';
                echo '<nickname>'.$user['nickname'].'</nickname>';
            echo '</member>';
        }
        echo '</members_present>';
		echo '</xmlresponse>';
		break;

	default:
		echo $usage;
		break;
}

mysql_close($con);

?>
