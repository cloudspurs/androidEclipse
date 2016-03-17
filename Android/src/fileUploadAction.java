import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.apache.struts2.ServletActionContext;

import com.opensymphony.xwork2.ActionSupport;

public class fileUploadAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private File upload;	// 上传的文件
	private String uploadContentType;	// 文件类型
	private String uploadFileName;		// 文件名
	private String savePath;			// 保存路径
	
	public void setSavePath(String path) {
		this.savePath = path;
	}
	// 获取上传文件的保存路径
	private String getSavePath() throws Exception {
		return ServletActionContext.getServletContext().getRealPath(savePath);
	}
	
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
		FileOutputStream fos = new FileOutputStream(getSavePath()
			+ "/" + getUploadFileName());
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
		
		return "success";	
	}
}
