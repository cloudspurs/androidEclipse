import com.opensymphony.xwork2.ActionContext;
import com.opensymphony.xwork2.ActionSupport;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;

import org.apache.commons.mail.DefaultAuthenticator;  
import org.apache.commons.mail.EmailException;       
import org.apache.commons.mail.SimpleEmail;

public class signupVeriCodeAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private String email;
	private String password;
	private String passwd;
	
	public String getEmail() {
		return email; 
	}
	public void setEmail(String email) {
		this.email = email;
	}
	
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	
	public String getPasswd() {
		return passwd;
	}
	public void setPasswd(String passwd) {
		this.passwd = passwd;
	}
	
	public String execute() throws Exception {
		// 获取数据库配置，生成Session
		Configuration conf = new Configuration().configure();
		ServiceRegistry serviceRegistry = new StandardServiceRegistryBuilder()
			.applySettings(conf.getProperties()).build();
		SessionFactory sf = conf.buildSessionFactory(serviceRegistry);
		Session sess = sf.openSession();
		
		// 查询用户信息
		Query result = sess.createQuery("from Users as u where u.email = :uemail");
		// 从网页获取用户名
		result.setParameter("uemail", getEmail());
		
		// 查询结果不为空，提示邮箱已注册
		if (result.list().size() != 0) {
			sess.close();
			sf.close();
			return "emailUsed";
		}
		
		// 获取两次输入的密码
		String password = getPassword();
		String passwd = getPasswd();
		
		// 验证两次输入密码是否相同
		if (password.equals(passwd) == false)
			return "error";
		
		// 将email和password存入session
		ActionContext.getContext().getSession().put("email",  getEmail());
		ActionContext.getContext().getSession().put("password", getPasswd());
		
		// 生成验证码
		randomNumber rn = new randomNumber();
		String veriCode = rn.generateString(4);
		
		// 将验证码存入session
		ActionContext.getContext().getSession().put("veriCode", veriCode);
		
		// 发送文本邮件验证码
		SimpleEmail email = new SimpleEmail();       
		//是否TLS校验，，某些邮箱需要TLS安全校验，同理有SSL校验
		//email.setTLS(true);   
		//email.setSSL(true); 
        email.setDebug(true);	// 打印调试信息
        // 设置SMTP服务器地址
        email.setHostName("smtp.163.com");
        // 设置账户密码
        email.setAuthenticator(new DefaultAuthenticator("18612481825@163.com", "qydg45683968"));  
        try {    
        	email.setFrom("18612481825@163.com"); 	//发送方,这里可以写多个  
        	email.addTo(getEmail()); 		// 接收方  
        	//email.addCc("443051430@qq.com"); 		// 抄送方  
        	//email.addBcc("443051430@qq.com"); 	// 秘密抄送方  
        	email.setCharset("utf-8");  
        	email.setSubject("验证码"); 				// 标题  
        	email.setMsg(veriCode);					// 内容  
        	email.send();  
        	System.out.println("发送成功");  
        } catch (EmailException e) {    
            e.printStackTrace();    
        }     
		
		return "success";
	}
}
