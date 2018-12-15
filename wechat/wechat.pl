#!/usr/bin/env perl
use Mojo::Weixin;
$host = "0.0.0.0";
$port = 3000;
$post_api = 'http://0.0.0.0:5001/post_api';

$client->load("Openwx",data=>{
    listen=>[{host=>$host,port=>$port}],
    post_stdout => 0,
    post_api=>$post_api,
    post_event => 1,
    post_event_list => ['login','stop','state_change','input_qrcode'],
});
$client->run();
