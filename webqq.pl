#!/usr/bin/env perl
use Mojo::Webqq;
$host = "0.0.0.0";
$port = 5000;
$post_api = 'http://127.0.0.1:5001/post_api';

my $client = Mojo::Webqq->new(
    allow_message_sync => 1,
);
$client->load("Openqq",data=>{
    listen=>[{host=>$host,port=>$port}],
    post_stdout => 0,
    post_api=>$post_api,
    post_event => 1,
    post_event_list => ['login','stop','state_change','input_qrcode'],
});
$client->run();
