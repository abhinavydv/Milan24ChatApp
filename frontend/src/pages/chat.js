import { useState, useEffect, useContext } from "react";
import ContactsList from "../components/ContactsList";
import ChatWindow from "../components/ChatWindow";
import { AuthContext } from "../contexts/AuthContext";
import axios from "axios";

export default function ChatPage() {
  const { user, logout } = useContext(AuthContext);
  const [contacts, setContacts] = useState([]);
  const [selectedContact, setSelectedContact] = useState(null);

  useEffect(() => {
    if (user) {
      fetchContacts();
    }
  }, [user]);

  const fetchContacts = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/contacts`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setContacts(res.data.map((contact) => contact.contact));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex h-screen">
      <div className="w-full md:w-1/3 lg:w-1/4 bg-white border-r">
        <div className="p-4 border-b flex justify-between items-center">
          <h1 className="text-xl font-semibold">Chats</h1>
          <button onClick={logout} className="text-sm text-red-500">
            Logout
          </button>
        </div>
        <ContactsList contacts={contacts} selectContact={setSelectedContact} />
      </div>
      <div className="flex-1">
        {selectedContact ? (
          <ChatWindow contact={selectedContact} />
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Select a contact to start chatting</p>
          </div>
        )}
      </div>
    </div>
  );
}
