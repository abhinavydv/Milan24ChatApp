export default function ContactsList({ contacts, selectContact }) {
  const [isAdding, setIsAdding] = useState(false);

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b flex items-center justify-between">
        <h2 className="text-lg font-medium">Contacts</h2>
        <button
          className="text-blue-500 hover:text-blue-700"
          onClick={() => setIsAdding(!isAdding)}
        >
          {isAdding ? "Cancel" : "Add"}
        </button>
      </div>
      {isAdding && <AddContactForm />}
      <ul className="flex-1 overflow-y-auto">
        {contacts.map((contact) => (
          <li
            key={contact.id}
            className="p-4 hover:bg-gray-100 cursor-pointer"
            onClick={() => selectContact(contact)}
          >
            <div className="flex items-center">
              <img
                src={contact.picture || "/default-avatar.png"}
                alt={contact.name}
                className="w-10 h-10 rounded-full mr-3"
              />
              <div>
                <p className="font-medium">{contact.name}</p>
                <p className="text-sm text-gray-500">{contact.email}</p>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
