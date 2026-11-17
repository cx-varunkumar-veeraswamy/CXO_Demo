<?php
// INTENTIONALLY VULNERABLE - vulnerable OSS functions are INVOKED with request data (SCA exploitable-path demo).
require 'vendor/autoload.php';

$twig = new \Twig\Environment(new \Twig\Loader\ArrayLoader([]));
echo $twig->createTemplate($_GET['t'])->render([]);                 // twig 1.35.0 sandbox/SSTI

$mail = new PHPMailer();
$mail->setFrom($_POST['from']);                                     // phpmailer 5.2.0 CVE-2016-10033 RCE via sender
$mail->addAddress($_POST['to']); $mail->send();

$client = new \GuzzleHttp\Client();
echo $client->request('GET', $_GET['u'], ['proxy' => $_GET['p']])->getBody();   // guzzle 6.3.0 httpoxy / SSRF

$log = new \Monolog\Logger('x');
$log->pushHandler(new \Monolog\Handler\StreamHandler($_GET['f']));  // monolog 1.22.0 user-controlled log path
$log->error($_GET['m']);
