import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.dom4j.io.XMLWriter;

public class xmlAction {
	 
	public static void createXml(userInfo userinfo, String file) {  
        try {
        	
            // 创建Document对象  
            Document document = DocumentHelper.createDocument();  
            
            // 添加根节点users
            Element rootElement = document.addElement("users");  
            // 添加根节点信息  
            rootElement.setText("用户信息");
            // 添加子节点email
            Element element = rootElement.addElement("email"); 
            element.setText(userinfo.getEmail());
            
            // 将document文档写入user.xml文件
            Writer fileWriter = new FileWriter(file);  
            //dom4j提供了专门写入文件的对象XMLWriter  
            XMLWriter xmlWriter = new XMLWriter(fileWriter);  
            xmlWriter.write(document);  
            xmlWriter.flush();  
            xmlWriter.close();
            
            // 将document文档对象直接转换成字符串输出 
            System.out.println(document.asXML());
            
            System.out.println("xml文档添加成功！");  
            
        } catch (IOException e) {  
            e.printStackTrace();  
        }  
	}
	
	public userInfo readXml(String file){
		
		userInfo userinfo = new userInfo();
        try{
        	//新建SaxReader对象，读取XML文档   
            SAXReader saxReader = new SAXReader();  
               
            Document document = saxReader.read(new File(file));	// 必须指定文件的绝对路径  
              
            //获取根节点对象  
            Element rootElement = document.getRootElement();
            
            System.out.println(document.asXML());
            
            //获取子节点  
            Element element = rootElement.element("email");  
            if(element != null){  
            	userinfo.setEmail(element.getText());
            }  
            
        } catch (Exception e) {    
            e.printStackTrace();    
        }
        
        return userinfo;
    }

}

 