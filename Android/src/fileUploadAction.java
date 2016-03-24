import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.apache.commons.mail.DefaultAuthenticator;
import org.apache.commons.mail.EmailException;
import org.apache.commons.mail.MultiPartEmail;
import org.apache.commons.mail.EmailAttachment;
import org.apache.struts2.ServletActionContext;
import com.opensymphony.xwork2.ActionSupport;

public class fileUploadAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private File upload;	// 上传的文件
	private String uploadFileName;		// 文件名
	private String uploadContentType;	// 文件类型

/* *******************************************************************	
	private String savePath;			// 保存路径
	public void setSavePath(String path) {
		this.savePath = path;
	}
	// 获取上传文件的保存路径
	private String getSavePath() throws Exception {
		return ServletActionContext.getServletContext().getRealPath(savePath);
	}
*********************************************************************** */
	
	public void setUpload(File upload) {
		this.upload = upload;
	}
	public File getUpload() {
		return(this.upload);
	}

	public void setUploadContentType(String uploadContentType) {
		this.uploadContentType = uploadContentType;
	}
	public String getUploadContentType() {
		return(this.uploadContentType);
	}
	
	public void setUploadFileName(String uploadFileName) {
		this.uploadFileName = uploadFileName;
	}
	public String getUploadFileName() {
		return(this.uploadFileName);
	}
	
	public String execute() throws Exception {
		// 防止没选中文件直接上传
		if(getUpload() == null) {
			return "input";
		}
		
		// 新建上传后的文件做为输出流，接收上传文件
		FileOutputStream fos = new FileOutputStream("/home/mqg/android/relda/" + getUploadFileName());
		// 把上传文件作为输入流
		FileInputStream fis = new FileInputStream(getUpload());
		// 设置缓冲
		byte[] buffer = new byte[1024];
		int len = 0;
		// 上传文件
		while ((len = fis.read(buffer)) > 0) {
			fos.write(buffer, 0, len);
		}
		fos.close();
		fis.close();
		
/*
		String command ="scp " + getUploadFileName() +" root@121.42.139.144:/root/cloud/java";
		String cmd[] = {"/bin/sh", "-c", command};
		File dir = new File(getSavePath());
		
		try {
			Runtime runtime = Runtime.getRuntime();
			Process process = runtime.exec(cmd, null, dir);
			// 取得命令结果的输出流  
		    InputStream is = process.getInputStream();  
		    // 用一个读输出流类去读  
		    InputStreamReader isr = new InputStreamReader(is);  
		    // 用缓冲器读行  
		    BufferedReader br = new BufferedReader(isr);  
		    String line = null;  
		    while ((line = br.readLine()) != null) {  
		        System.out.println(line);  
		    }  
		    is.close();  
		    isr.close();  
		    br.close();  
		} catch (IOException e) {  
		    e.printStackTrace();  
		}
		
		String name = getUploadFileName().toString();
		name = name.substring(0, name.length() - 5);
		name = name + ".class";
		
		command = "scp " + "root@121.42.139.144:/root/cloud/java/" + name + " /home/cloud/cloud";
		String cmdBack[] = {"/bin/sh", "-c", command};
		
		try {
			Thread.sleep(5000);
		} catch(InterruptedException e) {
			e.printStackTrace();
		}
		
		try {
			Runtime runtime = Runtime.getRuntime();
			Process process = runtime.exec(cmdBack);
			// 取得命令结果的输出流  
		    InputStream is = process.getInputStream();  
		    // 用一个读输出流类去读  
		    InputStreamReader isr = new InputStreamReader(is);  
		    // 用缓冲器读行  
		    BufferedReader br = new BufferedReader(isr);  
		    String line = null;  
		    while ((line = br.readLine()) != null) {  
		        System.out.println(line);  
		    }  
		    is.close();  
		    isr.close();  
		    br.close();  
		} catch (IOException e) {  
		    e.printStackTrace();  
		}
		
		MultiPartEmail email = new MultiPartEmail();       
		//是否TLS校验，，某些邮箱需要TLS安全校验，同理有SSL校验
		//email.setTLS(true);   
		//email.setSSL(true); 
        email.setDebug(true);	// 打印调试信息
        // 设置SMTP服务器地址
        email.setHostName("smtp.163.com");
        // 设置账户密码
        email.setAuthenticator(new DefaultAuthenticator("18612481825@163.com", "qydg45683968"));  
        try {
        	// 新建附件
        	EmailAttachment attachment = new EmailAttachment();
        	attachment.setPath("/home/cloud/cloud/" + name);  
        	attachment.setDisposition(EmailAttachment.ATTACHMENT);  
        	attachment.setDescription(name);  
        	attachment.setName(name);
        	email.setFrom("18612481825@163.com"); 	//发送方,这里可以写多个  
        	email.addTo("443051430@qq.com"); 		// 接收方  
        	//email.addCc("443051430@qq.com"); 		// 抄送方  
        	//email.addBcc("443051430@qq.com"); 	// 秘密抄送方  
        	email.setCharset("utf-8");  
        	email.setSubject("result"); 				// 标题  
        	email.setMsg("result");
        	email.attach(attachment);
        	email.send();  
        	System.out.println("发送成功");  
        } catch (EmailException e) {    
            e.printStackTrace();    
        }
*/		
		return "success";	
	}
}
