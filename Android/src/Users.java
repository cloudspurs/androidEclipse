import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity		// 持久化类声明
@Table(name="Users")	// 制定该类映射的表

public class Users {
	@Id		// 制定该类的表示属性
	// 指定主键生成策略（自动增长）
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	
	private Integer id;
	private String email;
	private String password;
		
	public void setId(Integer id) {
		this.id = id;
	}
	public Integer getId() {
		return this.id;
	}
	
	public void setEamil(String email) {
		this.email = email;
	}
	public String gerEmail() {
		return this.email;
	}
	
	public void setPassword(String password) {
		this.password = password;
	}
	public String getPassword() {
		return this.password;
	}
}
