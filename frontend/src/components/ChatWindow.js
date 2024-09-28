import { useState, useEffect, useContext } from "react";
import { io } from "socket.io-client";
import { AuthContext } from "../contexts/AuthContext";
import axios from "axios";

export default function ChatWindow({ contact }) {
  const { user } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const socket = useRef(null);

  useEffect(() => {
    fetchMessages();

    const token = localStorage.getItem("access_token");
    socket.current = io(process.env.NEXT_PUBLIC_BACKEND_URL, {
      query: { user_id: user.id },
      auth: { token },
      transports: ["websocket"],
    });

    socket.current.emit("join", { user_id: user.id });

    socket.current.on("new_message", (data) => {
      if (data.from_user_id === contact.id) {
        setMessages((prev) => [...prev, data]);
      }
    });

    return () => {
      socket.current.disconnect();
    };
  }, [contact]);

  const fetchMessages = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/message/conversation/${contact.id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessages(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSendMessage = async () => {
    if (newMessage.trim() === "") return;
    try {
      const token = localStorage.getItem("access_token");
      await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/message/send`,
        { to_user_email: contact.email, content: newMessage },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setNewMessage("");
      setMessages((prev) => [
        ...prev,
        {
          from_user_id: user.id,
          to_user_id: contact.id,
          content: newMessage,
          timestamp: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b flex items-center">
        <img
          src={contact.picture || "/default-avatar.png"}
          alt={contact.name}
          className="w-10 h-10 rounded-full mr-3"
        />
        <h2 className="text-lg font-medium">{contact.name}</h2>
      </div>
      <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-4 flex ${
              msg.from_user_id === user.id ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                msg.from_user_id === user.id
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
      </div>
      <div className="p-4 border-t">
        <div className="flex">
          <input
            className="flex-1 p-2 border rounded-l-lg"
            placeholder="Type a message..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                handleSendMessage();
              }
            }}
          />
          <button
            className="bg-blue-500 text-white p-2 rounded-r-lg"
            onClick={handleSendMessage}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
