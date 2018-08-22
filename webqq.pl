#!/usr/bin/env perl
use Mojo::Webqq;
use Digest::MD5 qw(md5_hex);
$host = "0.0.0.0";				#发送消息接口监听地址，没有特殊需要请不要修改
$port = 5000;					#发送消息接口监听端口，修改为自己希望监听的端口
$post_api = 'http://127.0.0.1:5001/post_api',	#可选，接收消息或事件的上报地址
my $client=Mojo::Webqq->new(
    account     => 1054855541,			#QQ账号
    pwd         => md5_hex('tzw19990401'),	#登录密码
    http_debug  =>  0,				#是否打印详细的debug信息
    log_level   =>  "info",			#日志打印级别，debug|info|msg|warn|error|fatal
    login_type  =>  "login",			#登录方式，login 表示账号密码登录
);
# $client->load("ShowMsg");			#客户端加载ShowMsg插件，用于打印发送和接收的消息到终端
$client->load("Openqq",data=>{
		listen=>[{host=>$host,port=>$port}],
		post_stdout => 0,	#可选，上报数据是否打印到stdout，适合管道交互信息方式，默认0
		post_api=>$post_api,
		post_event => 1,		#可选，是否上报事件，为了向后兼容性，默认值为1
		post_event_list => ['login','stop','state_change','input_qrcode'],  #可选，上报事件列表
	});
#$client->load("IRCShell",data=>{
#listen=>[ {host=>"0.0.0.0",port=>6667}], #监听6697端口
#load_friend => 1, #可选,是否初始为每个好友生成irc虚拟帐号并加入频道 #我的好友
#});
$client->run();					#客户端开始运行

