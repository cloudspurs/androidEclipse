import java.io.InputStream;
import org.apache.struts2.ServletActionContext; 
import com.opensymphony.xwork2.ActionSupport;

public class RLResult1DownloadAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private String inputPath;
	
	public String getInputPath() {
		return inputPath;
	}
	public void setInputPath(String inputPath) {
		this.inputPath = inputPath;
	}
	
	public InputStream getTargetFile() throws Exception {
		return ServletActionContext.getServletContext()
				.getResourceAsStream(inputPath);
	}
	
	public String execute() throws Exception {
		return "success";
    }
}
