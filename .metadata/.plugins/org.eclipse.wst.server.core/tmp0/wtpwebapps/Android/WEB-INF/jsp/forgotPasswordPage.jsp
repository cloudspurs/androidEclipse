<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="shortcut icon" href="assets/ico/favicon.png">
<title>忘记密码</title>
<link href="assets/css/bootstrap.css" rel="stylesheet">
<link href="assets/css/cloud.css" rel="stylesheet">
<link href="assets/css/bootstrap-responsive.css" rel="stylesheet"> 
</head>

<body class="padding-body">
   <div class="container">
        <form action="sendVariCode" onsubmit="return check3(this);" class="form-signin">
            <h2 class="form-signin-heading text-center">修改密码</h2>
            <input type="text" name="email" placeholder="请输入邮箱，重置密码" class="input-block-level">
            <button type="submit" class="btn btn-block btn-large btn-success">发送</button>
        </form>
    </div>      
<script src="assets/js/cloud.js"></script>
<script src="assets/js/jquery.js"></script> 
<script src="assets/js/bootstrap.min.js"></script>
</body>
</html>
