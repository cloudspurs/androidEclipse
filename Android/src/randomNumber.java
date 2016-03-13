import java.util.Random;
public class randomNumber {
	public static final String allChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	
	// 生成length长度随机验证码
	public String generateString(int length) {
		StringBuffer sb = new StringBuffer();
		Random random = new Random();
		
		for (int i = 0; i < length; i++) {
			sb.append(allChar.charAt(random.nextInt(allChar.length())));
		}
		
		return sb.toString();
	}

}
