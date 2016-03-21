<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="s" uri="/struts-tags"%>    
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
        	<li><a class="brand" href="#">ISCAS</a></li>
        	<!-- 
            <li><a href="<s:url action="managePage"/>">管理</a></li>
            -->           
        </ul>
        <form class="navbar-search pull-right">
            <input type="text" class="search-query" placeholder="Search">
        </form>
    </div>
    </div>  
    </div>
    </div>   

    <div class="container">
        <ul class="nav nav-tabs">
            <li class="active"><a href="#tab0" data-toggle="tab">Android</a></li>
            <li><a href="#tab1" data-toggle="tab">Resource Leak</a></li>
        </ul>
        <div class="tab-content">
            <div id="tab0" class="active tab-pane h-div">
            <!-- 文件上传表单 -->
	            <form action="Upload" method="post" enctype="multipart/form-data">
	            	<input type="file" name="upload">
	            	<s:fielderror></s:fielderror>
	            	<button type="submit">上传</button>
	            </form>	
            </div>
            
            <div id="tab1" class="tab-pane h-div">
            <div class="container-fluid">
            <div class="row-fluid">
                <div class="span4 text-center">
            		<a href="<s:url action="RLExample1"/>">onActivityResult</a> 	 
            	</div>
            	<div class="span4 text-center">
            	 	<a href="<s:url action="RLExample2"/>">onClick</a>  
            	</div>
            	<div class="span4 text-center">
            		<a href="<s:url action="RLExample3"/>">onClickOnClick</a> 
            	</div>	 
            </div>
            </div>	
            </div>
        </div>
    </div>
   
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