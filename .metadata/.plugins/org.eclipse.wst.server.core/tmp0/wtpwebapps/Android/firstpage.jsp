<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="s" uri="/struts-tags"%>    
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<!-- IE8专用标记 -->
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!-- Bootstrap设置 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- 浏览器标签页小图标 -->
<link rel="shortcut icon" href="assets/ico/favicon.png">
<title>首页</title>
<link href="assets/css/bootstrap.css" rel="stylesheet">
<link href="assets/css/docs.css" rel="stylesheet">
<link href="assets/css/cloud.css" rel="stylesheet">
<link href="assets/css/bootstrap-responsive.css" rel="stylesheet">
</head>

<body data-spy="scroll" data-target=".bs-docs-sidebar">
    <div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
    <div class="container">
    	<!-- 页面缩小时导航条样式 -->
    	<button type="button" class="btn btn-navbar collapsed" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
        </button>
    <div class="nav-collapse collapse">
    	<!-- 导航条 -->
        <ul class="nav">
        	<li><a class="brand" href="http://www.iscas.ac.cn/">ISCAS</a></li>
            <li><a href="<s:url action="signinPage"/>">登录</a></li>
            <li><a href="<s:url action="signupPage"/>">注册</a></li>           
        </ul>
        <!-- 搜索框 -->
        <form class="navbar-search pull-right">
            <input type="text" class="search-query" placeholder="Search">
        </form>
    </div>
    </div>  
    </div>
    </div>

	<!-- 滑动框 -->
    <div id="myCarousel" class="carousel slide h1-div">
        <ol class="carousel-indicators">
            <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
<!--            
            <li data-target="#myCarousel" data-slide-to="1"></li>
            <li data-target="#myCarousel" data-slide-to="2"></li>
-->
        </ol>
        <div class="carousel-inner">
            <div class="active item">
            	<div class="jumbotron masthead">
			    	<div class="container">
				        <h1>Android</h1>
				        <h2>方便、快捷的静态测试</h2>
				        <h2>让APK开发更迅速、简单</h2>
				        <p>Join us</p>
				      	<p>使用文档</p>
			      	</div>
			    </div>
            </div>
<!--
            <div class="item">222222222222222222222222222222222222</div>
            <div class="item">333333333333333333333333333333333333</div>
-->
        </div>
        <a class="carousel-control left" href="#myCarousel" data-slide="prev">&lsaquo;</a>
        <a class="carousel-control right" href="#myCarousel" data-slide="next">&rsaquo;</a>
    </div>
	<!-- 页脚 -->
    <footer class="footer"> 
    <div class="container">
        <p>ISCAS · Android APK Static Analysis</p>
        <ul class="footer-links">
            <li><a href="#">BLOG</a>
            <li>·</li>
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
    