import com.opensymphony.xwork2.ActionContext;
import com.opensymphony.xwork2.ActionSupport;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;

public class signupAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private String veriCode;
	
	public String getVeriCode() {
		return veriCode;
	}
	public void setVeriCode(String veriCode) {
		this.veriCode = veriCode;
	}
	
	public String execute() throws Exception {
		// 取出之前保存的验证码
		String veriCode = (String)(ActionContext.getContext().getSession().get("veriCode"));
		
		// 判断验证码是否正确
		if (veriCode.equals(getVeriCode()) == false)
			return "input";
		
		// 从session取出email和password
		String email = (String)ActionContext.getContext().getSession().get("email");
		String password = (String)ActionContext.getContext().getSession().get("password");
		
		// 新建用户
		Users user = new Users();
		user.setEamil(email);
		user.setPassword(password);
		
		// 获取数据库配置，生成Session
		Configuration conf = new Configuration().configure();
		ServiceRegistry serviceRegistry = new StandardServiceRegistryBuilder()
			.applySettings(conf.getProperties()).build();
		SessionFactory sf = conf.buildSessionFactory(serviceRegistry);
		Session sess = sf.openSession();
		Transaction tx = sess.beginTransaction();
		
		//将user存入数据库
		sess.save(user);	
		tx.commit();
		
		sess.close();
		sf.close();
		
		return "success";
	}
}
