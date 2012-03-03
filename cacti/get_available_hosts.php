<?php

include('hosts_alive_sql.php');

$get = $argv['1'];
$parameters = array('all', 'members', 'unknown', 'member_devices');

if ( !in_array($get, $parameters) )
	exit("Parameter not available \n");


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


switch ($get) {
    case 'all':
        $query = $hostQueries['all'];
	echo get_hosts_alive($con, $query, $db) . "\n";
        break;

    case 'members':
        $query = $hostQueries['members'];
	echo get_hosts_alive($con, $query, $db) . "\n";
        break;

    case 'unknown':
        $query = $hostQueries['unknown'];
	echo get_hosts_alive($con, $query, $db) . "\n";
        break;

    case 'member_devices':
        $query = $hostQueries['member_devices'];
	echo get_hosts_alive($con, $query, $db) . "\n";	
	break;

    default: 
	echo "Wrong Parameter used.";
}


exit(1);
?>
