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
<title>注册</title>
<link href="assets/css/bootstrap.css" rel="stylesheet">
<link href="assets/css/cloud.css" rel="stylesheet">
<link href="assets/css/bootstrap-responsive.css" rel="stylesheet"> 
</head>
<body class="padding-body">
    <div class="container">
        <form action="signupVeriCode" onsubmit="return check2(this);" class="form-signin">
            <h3 class="form-signin-heading text-center">创建个人账户</h3>
            <input type="text" name="email" placeholder="邮箱" class="input-block-level">
            <input type="password" name="password" placeholder="密码" class="input-block-level">
            <input type="password" name="passwd" placeholder="确认密码" class="input-block-level">
            <p class="form-signin-heading">点击“注册”按钮，代表您同意服务条款和  
            	<a href="<s:url action="privacyPage"/>">隐私条款</a>!
            </p>
           	<button type="submit" class="btn btn-block btn-large btn-success">注册</button>
        </form>
    </div>
<script src="assets/js/cloud.js"></script>
<script src="assets/js/jquery.js"></script> 
<script src="assets/js/bootstrap.min.js"></script>     
</body>
</html>

