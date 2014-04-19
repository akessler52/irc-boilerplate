<?php

$_s['nick'] = '<NICKNAME>';
$nick = $_s['nick'];
$_s['user'] = '<USERNAME>';
$_s['name'] = '<REALNAME> c/o alex';

$_s['chan'] = array('<CHANNEL>');


$_s['host'] = 'localhost';
$_s['port'] = 6667;

date_default_timezone_set('America/Detroit');

function safe_feof($fp, &$start = null) {
	$start = microtime(true);
	return feof($fp);
	}

while (true) {
	echo ">>> Connecting to IRC socket\n";
	// Open IRC Socket
	$irc = fsockopen($_s['host'], $_s['port']);
	if ($irc === false) {
		echo "!!! [".date('r')."] Failed to open IRC socket. Sleeping 30 seconds\n";
		unset($irc);
		sleep(30);
		continue;
	}

	// Provide IRC information to the server
	fwrite($irc, "NICK $nick\r\n");
	fwrite($irc, "USER {$_s['user']} {$_s['host']} {$_s['host']} :{$_s['name']}\r\n");
	foreach ($_s['chan'] as $chan) {
		fwrite($irc, "JOIN $chan\r\n");
		}

	$_socket_start = null;
	$_socket_timeout = ini_get('default_socket_timeout');
	while (!safe_feof($irc, $_socket_start) && (microtime(true) - $_socket_start) < $_socket_timeout) {
		$raw = trim(fgets($irc));
		echo "$raw\n";
		
		// Handle ping/pong
		if (substr($raw, 0, 4) == 'PING') {
			fwrite($irc, 'PONG '.substr($raw, 5)."\r\n");
			echo ">>> PONG\n";
			continue;
		}

		// Analyze message
		// 1 - nick
		// 2 - user@host
		// 3 - command
		// 4 - channel
		// 5 - anything between the channel and message text
		// 6 - message text
		if (preg_match('/^:([^!]+)!([^ ]+) ([^ ]+) (#[^ ]+|) ?([^:]*):(.*)/', $raw, $parts) === 1) {
			$inick = $parts[1];
			$iuser = $parts[2];
			$command = ($parts[3] == 'PRIVMSG') ? null : $parts[3];
			$ichan = $parts[4];
			$mtext = trim($parts[6]);
			if (!mb_check_encoding($mtext, 'UTF-8')) {
				$mtext = mb_convert_encoding($mtext, 'UTF-8', 'UTF-8');
			}
		}
		else continue;

		/*
		 * main code goes here
		 */

	} // End IRC reader loop
	echo "!!! Broken pipe, sleeping 30 seconds\n";
	fclose($irc);
	unset($irc);
	sleep(30);

} // End connection loop

?>
