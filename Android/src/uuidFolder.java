import java.util.UUID;

public class uuidFolder {

	private String folder;

	public String getFolder() {
		return folder;
	}

	public void setFolder(String folder) {
		this.folder = folder;
	}
	
	public uuidFolder() {
		String uuid = UUID.randomUUID().toString();
		uuid = uuid.replaceAll("-", "");
		folder = uuid;
	}
}
