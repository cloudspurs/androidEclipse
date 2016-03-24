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
<title>登录</title>
<link href="assets/css/bootstrap.css" rel="stylesheet">
<link href="assets/css/cloud.css" rel="stylesheet">
<link href="assets/css/bootstrap-responsive.css" rel="stylesheet">
</head>

<body class="padding-body">
    <div class="container">
    	<!-- check1(): 表单输入检查 -->
        <form action="signin" onsubmit="return check1(this);" class="form-signin">
            <h2 class="form-signin-heading text-center">登录</h2>
            <input type="text" name="email" class="input-block-level" placeholder="邮箱" tabindex="1">
            <a href="<s:url action="forgotPasswordPage"/>" class="pull-right">忘记密码</a>
            <input type="password" name="password" class="input-block-level"  placeholder="密码" tabindex="2">
            <button type="submit" class="btn btn-large btn-block btn-success" tabindex="3">登录</button>
        </form>
    </div>
<script src="assets/js/cloud.js"></script>
<script src="assets/js/jquery.js"></script> 
<script src="assets/js/bootstrap.min.js"></script>
</body>
</html>
