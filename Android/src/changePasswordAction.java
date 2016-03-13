import com.opensymphony.xwork2.ActionContext;
import com.opensymphony.xwork2.ActionSupport;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;

public class changePasswordAction extends ActionSupport {
	private static final long serialVersionUID = 1L;
	
	private String password;
	private String passwd;
	
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
		String password, passwd;
		password = getPassword();
		passwd = getPasswd();
		
		if (password.equals(passwd) == false)
			return "input";
		
		// 从session中取出用户邮箱
		String email;
		email = (String)ActionContext.getContext().getSession().get("email");
		
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
		
		Query result = sess.createQuery("from Users as u where u.email = :uemail");
		// 从网页获取用户名
		result.setParameter("uemail", email);
		
		Users u = (Users)result.list().get(0);
		
		user.setId(u.getId());
		
		// 更新数据库用户信息
		sess.merge(user);
		
		tx.commit();
		
		sess.close();
		sf.close();
		
		return "success";
	}
}
