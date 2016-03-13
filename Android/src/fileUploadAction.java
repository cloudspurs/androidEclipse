import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;

import org.apache.struts2.ServletActionContext;

import com.opensymphony.xwork2.ActionSupport;

public class fileUploadAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private File upload;	// 上传的文件
	private String uploadContentType;	// 文件类型
	private String uploadFileName;		// 文件名
	private String savePath;			// 保存路径
	
	// 读取struts.xml配置的文件保存路径信息
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
		if(getUpload() == null)
			return "input";
		
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
		return "success";	
	}
}
