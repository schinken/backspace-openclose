<?php


define('BCKSPC_URL',            'http://status.bckspc.de/status.php?response=json' );

define('BCKSPC_IMG_OPEN',       'status_open.png');
define('BCKSPC_IMG_CLOSED',     'status_closed.png');
define('BCKSPC_IMG_UNKNOWN',    'status_unknown.png');

define('BCKSPC_APC_NAME',       'bckspc_status_cache');
define('BCKSPC_APC_TIME',       300 );

/**
* Retrieve content from URL
*/

function curlStatus( $URL ) {

    $ch = curl_init( $URL );

    curl_setopt( $ch, CURLOPT_RETURNTRANSFER,   true                );
    curl_setopt( $ch, CURLOPT_USERAGENT     ,   'Backspace Website' );
    curl_setopt( $ch, CURLOPT_CONNECTTIMEOUT,   2                   );
    curl_setopt( $ch, CURLOPT_ENCODING      ,   'gzip,deflate'      );

    $Return = curl_exec( $ch );

    if( curl_getinfo($ch, CURLINFO_HTTP_CODE) != 200 ) {
        throw new Exception('Unable to retrieve status');
    }

    return $Return;
}


function retrieveStatus() {

    $Members = 0;

    try {

        // retrieve data from backspace URL
        $Result = curlStatus( BCKSPC_URL );

        // try to decode json
        // default format is:
        //    all: int
        //    members: int
        //    member_devices: int
        //    unknown_devices: int

        $decoded = @json_decode( $Result, true );
        if( $decoded === null ) {
            $Image = BCKSPC_IMG_UNKNOWN;
        } else {
            
            if( !isset( $decoded['members'] ) ) {
                $Image = BCKSPC_IMG_UNKNOWN;
            } else {

                $Members = (int) $decoded['members'];
                if( $Members == 0 ) {
                    $Image = BCKSPC_IMG_CLOSED;
                } else  {
                    $Image = BCKSPC_IMG_OPEN;
                }
            }
        }       

    } catch( Exception $e ) {
        $Image = BCKSPC_IMG_UNKNOWN;
    }

    return array(
        'members' => $Members,
        'image'   => $Image
    );
}

function getStatusArray() {

    // Check if apc has a cached snippet for me, to reduce curl calls to API
    $APC = apc_fetch( BCKSPC_APC_NAME );
    if( $APC === false ) {
        $Result = retrieveStatus();
        apc_store( BCKSPC_APC_NAME, $Result, BCKSPC_APC_TIME );
    } else {
        $Result = $APC;
    }

    return $Result;

}

