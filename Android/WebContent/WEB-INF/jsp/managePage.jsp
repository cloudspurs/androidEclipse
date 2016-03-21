<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="assets/ico/favicon.png">
    <title>主页</title>
	<link href="assets/css/bootstrap.css" rel="stylesheet">
	<link href="assets/css/docs.css" rel="stylesheet">
	<link href="assets/css/cloud.css" rel="stylesheet">
    <link href="assets/css/bootstrap-responsive.css" rel="stylesheet">
</head>
<body data-spy="scroll" data-target=".bs-docs-sidebar">
    <div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
    <div class="container">
        <button type="button" class="btn btn-navbar collapsed" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
        </button>
    <div class="nav-collapse collapse">
        <ul class="nav">
        	<li><a class="brand" href="http://www.iscas.ac.cn/">ISCAS</a></li>
         <li><a href="#">cloud</a></li>
            <li><a href="manage.jsp">管理</a></li>           
            <li><h4 class="offset1">Android Apps Online Test And Analysis Platform</h4></li>
        </ul>
        <form class="navbar-search pull-right">
            <input type="text" class="search-query" placeholder="搜索">
        </form>
    </div>
    </div>  
    </div>
    </div>
    
    <div class="container">
        <div class="row">
            <div class="span3 bs-docs-sidebar">
                 <ul class="nav nav-list bs-docs-sidenav affix">
                      <li><a href="#processing">分析中</a></li>
                      <li><a href="#queue">队列中</a></li>
                      <li><a href="#processed">历史记录</a></li>
                      <li><a href="#changePassword">修改密码</a></li>
                      <li><a href="#userinfo">个人信息</a></li>
                 </ul>
            </div>
            <div class="span9">
                <section id="processing">
                    <div class="page-header">
                        <h1>分析中APK</h1>
                    </div> 
                        <p>1111111111111111111</p>
                        <p>2222222222222222222</p>
                        <p>3333333333333333333</p>        
                </section>
                 <section id="queue">
                    <div class="page-header">
                        <h1>队列中APK</h1>
                    </div> 
                        <p>1111111111111111111</p>
                        <p>2222222222222222222</p>
                        <p>3333333333333333333</p>        
                </section>
                <section id="processed">
                    <div class="page-header">
                        <h1>历史记录</h1>
                    </div> 
                        <p>1111111111111111111</p>
                        <p>2222222222222222222</p>
                        <p>3333333333333333333</p>        
                </section>
                <section id="changePassword">
                    <div class="page-header">
                        <h1>修改密码</h1>
                    </div> 
                    <input placeholder="新密码">
                    <input placeholder="确认密码">
                   <button class="btn">确定</button>
                </section>
                <section id="userinfo">
                    <div class="page-header">
                        <h1>个人信息</h1>
                    </div> 
                        <p>1111111111111111111</p>
                        <p>2222222222222222222</p>
                        <p>3333333333333333333</p>        
                </section>
           </div>
        </div>
    </div>
 
    <footer class="footer"> 
    <div class="container">
        <p>ISCAS</p>
        <p>Android APK Static Analysis</p>
        <p>Version:12-25</p>
        <ul class="footer-links">
            <li><a href="#">Blog</a>
            <li><a href="#">Forum</a>
        </ul>
    </div>
    </footer>
<script src="assets/js/jquery.js"></script> 
<script src="assets/js/bootstrap.min.js"></script>
<script src="assets/js/holder/holder.js"></script>
<script src="assets/js/application.js"></script>
</body>
</html>
