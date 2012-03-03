<?php

include('hosts_alive_sql.php');

$usage = "Use: " . $_SERVER['PHP_SELF'] . "?response=[json|xml|img]";

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
		'all' => get_hosts_alive($con, $hostQueries['all'], $db),
		'members' => get_hosts_alive($con, $hostQueries['members'], $db),
		'member_devices' => get_hosts_alive($con, $hostQueries['member_devices'], $db),
		'unknown_devices' => get_hosts_alive($con, $hostQueries['unknown'], $db)
	      );


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
		echo json_encode($hosts);
		break;

	case "xml":
		header("Content-type: text/xml");
		echo '<?xml version="1.0" encoding="utf-8" ?>';
		echo '<xmlresponse>';
		echo '<alive_hosts>' . $hosts['all'] . '</alive_hosts>';
		echo '<members>' . $hosts['members'] . '</members>';
		echo '<member_devices>' . $hosts['member_devices'] . '</member_devices>';
		echo '<unknown_devices>' . $hosts['unknown_devices'] . '</unknown_devices>';
		echo '</xmlresponse>';
		break;

	default:
		echo $usage;
		break;
}

mysql_close($con);

?>
