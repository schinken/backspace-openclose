<?php

require_once 'get.php';

$Result = getStatusArray();

?>
<!DOCTYPE html>
<html>
    <head>
        <title>Backspace Online Status</title>
        <style type="text/css">

            *, html, body {
             margin: 0; padding: 0;
            }

            #status {
                display: inline-block;
                position: relative;

                text-align: center;

                width: 166px;
                height: 90px;
            }

            #members {
                -webkit-border-radius: 8px;
                -moz-border-radius: 8px;
                -o-border-radius: 8px;
                border-radius: 8px;

                -webkit-box-shadow: 0 0 10px rgba(0,0,0,0.4);
                -moz-box-shadow: 0 0 10px rgba(0,0,0,0.4);
                -o-box-shadow: 0 0 10px rgba(0,0,0,0.4);
                box-shadow: 0 0 10px rgba(0,0,0,0.4);

                background-color: #fff;
                border: 2px solid #000;

                padding: 1px 10px;
                margin-right: 5px;
                margin-top: 69px;

                font-family: Verdana;
                font-size: 10px;

                display: inline-block;
            }
        </style>
    </head>
    <body>
        <div id="status" style="background-image: url(<?php echo $Result['image']; ?>)">
            <?php if( $Result['members'] > 0 ): ?>
                <div id="members" title="Currently are <?php echo $Result['members']; ?> Members present"><?php echo $Result['members']; ?></div>
            <?php endif; ?>
        </div>
    </body>
</html>
