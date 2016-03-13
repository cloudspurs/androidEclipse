import com.opensymphony.xwork2.*;

public class confirmVeriCodeAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private String veriCode;
	
	public String getVeriCode() {
		return veriCode;
	}
	public void setVariCode(String veriCode) {
		this.veriCode = veriCode;
	}
	
	public String execute() throws Exception {
		String veriCode = (String)(ActionContext.getContext().getSession().get("veriCodeFP"));
		
		if (veriCode.equals(getVeriCode()) == false)
			return "success";
		else
			return "input";
	}
}
