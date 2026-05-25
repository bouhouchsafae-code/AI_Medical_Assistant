"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import {
  Bot,
  Send,
  MessageSquare
} from "lucide-react";
import { useRouter } from "next/navigation";

export default function PatientDashboard() {

  const router = useRouter();

  const [patientData, setPatientData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // =========================
  // 🤖 AI CHAT STATES
  // =========================

  const [chatMessages, setChatMessages] =
    useState<any[]>([]);

  const [showChat, setShowChat] =
    useState(false);

  const [chatInput, setChatInput] =
    useState("");

  const [chatLoading, setChatLoading] =
    useState(false);

  // =========================
  // 💬 DOCTOR CHAT
  // =========================

  const [showMessages, setShowMessages] =
    useState(false);

  const [doctorMessages, setDoctorMessages] =
    useState<any[]>([]);

  const [messageInput, setMessageInput] =
    useState("");

  // =========================
  // 🚀 LOAD DATA
  // =========================

  useEffect(() => {

    fetchAnalyses();

    fetchMessages();

  }, []);

  // =========================
  // 📦 LOAD ANALYSES
  // =========================

  const fetchAnalyses = async () => {

    try {

      const token =
        localStorage.getItem("token");

      const response = await axios.get(

        "http://127.0.0.1:8000/my-analyses",

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }

      );
      console.log(response.data);
      console.log(
        "ANALYSES:",
        response.data
      );

      setPatientData(response.data);

    }

    catch (err) {

      console.log(err);

    }

    finally {

      setLoading(false);

    }

  };

  // =========================
  // 💬 LOAD DOCTOR MESSAGES
  // =========================

  const fetchMessages = async () => {

    try {

      const token =
        localStorage.getItem("token");

      const user = JSON.parse(
        localStorage.getItem("user") || "{}"
      );

      const doctorId =
        user.assigned_doctor_id;

      if (!doctorId) return;

      const response = await axios.get(

        `http://127.0.0.1:8000/messages/${doctorId}`,

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }

      );

      setDoctorMessages(
        response.data.messages
      );

    }

    catch (err) {

      console.log(err);

    }

  };

  // =========================
  // 💬 SEND MESSAGE
  // =========================

  const sendDoctorMessage = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    if (!messageInput.trim()) return;

    try {

      const token =
        localStorage.getItem("token");

      const user = JSON.parse(
        localStorage.getItem("user") || "{}"
      );

      await axios.post(

        "http://127.0.0.1:8000/send-message",

        {
          receiver_id:
            user.assigned_doctor_id,

          content: messageInput
        },

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }

      );

      setMessageInput("");

      fetchMessages();

    }

    catch (err) {

      console.log(err);

    }

  };

  // =========================
  // 🤖 EXACT CHATBOT
  // =========================

  const handleSendMessage = async () => {

    if (!chatInput.trim()) return;

    const messageToSend = chatInput;

    setChatInput("");

    const userMessage = {

      role: "user",

      content: messageToSend

    };

    setChatMessages((prev) => [

      ...prev,

      userMessage

    ]);

    setChatLoading(true);

    try {

      const token =
        localStorage.getItem("token");

      const response = await axios.post(

        "http://127.0.0.1:8000/ai/chat",

        {
          message: messageToSend
        },

        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }

      );

      console.log(response.data);

      const aiMessage = {

        role: "assistant",

        content:
          response.data.response ||
          response.data.reply ||
          "No response from AI"

      };

      setChatMessages((prev) => [

        ...prev,

        aiMessage

      ]);

    }

    catch (error: any) {

      console.log(error);

      const errorMessage = {

        role: "assistant",

        content:
          "Backend connection error"

      };

      setChatMessages((prev) => [

        ...prev,

        errorMessage

      ]);

    }

    finally {

      setChatLoading(false);

    }

  };

  // =========================
  // 🚪 LOGOUT
  // =========================

  const handleLogout = () => {

    localStorage.removeItem("token");

    localStorage.removeItem("user");

    router.push("/");

  };
  const analyses = patientData?.analyses || [];

  return (

    <main className="min-h-screen bg-black text-white p-8">

      {/* HEADER */}

      <div className="flex items-center justify-between mb-10">

        <div>

          <h1 className="text-4xl font-bold">

            Patient Dashboard

          </h1>

          <p className="text-gray-400 mt-2">

            View your medical analyses
            and reports

          </p>

        </div>

        <div className="flex gap-4">

          <button

            onClick={() =>
              setShowMessages(
                !showMessages
              )
            }

            className="bg-green-500 hover:bg-green-400 transition px-6 py-3 rounded-2xl font-semibold text-black"

          >

            Chat With Doctor

          </button>

          <button

            onClick={handleLogout}

            className="bg-red-500 hover:bg-red-400 transition px-6 py-3 rounded-2xl font-semibold text-white"

          >

            Logout

          </button>

        </div>

      </div>

      {/* ANALYSES */}

      {/* ========================= */}
    {/* PATIENT ANALYSES */}
    {/* ========================= */}

    {loading ? (

      <div className="text-gray-400 text-lg">

        Loading analyses...

      </div>

    ) : analyses.length === 0 ? (

      <div className="bg-[#111111] border border-gray-800 rounded-3xl p-10 text-center text-gray-400">

        No analyses linked to this patient

      </div>

    ) : (

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">

        {analyses.map((analysis: any) => (

          <div

            key={analysis.id}

            className="bg-[#111111] border border-gray-800 rounded-3xl overflow-hidden shadow-xl"

          >

            {/* IMAGE */}

            <img

              src={analysis.image_url}

              alt="analysis"

              className="w-full h-64 object-cover"

            />

        {/* CONTENT */}

        <div className="p-6">

          <h2 className="text-2xl font-bold mb-3 text-white">

            {analysis.prediction ||
             analysis.diagnosis ||
             "Medical Analysis"}

          </h2>

          <p className="text-cyan-400 mb-2">

            Confidence:
            {" "}
            {analysis.confidence
              ? `${(
                  analysis.confidence * 100
                ).toFixed(1)}%`
              : "N/A"}

          </p>

          <p className="text-gray-500 text-sm mb-6">

            {analysis.created_at}

          </p>

          {/* BUTTONS */}

          <div className="flex gap-3">

            {/* PDF */}

            {analysis.pdf_url && (

              <a

                href={analysis.pdf_url}

                target="_blank"

                className="flex-1 bg-cyan-500 hover:bg-cyan-400 transition rounded-xl py-3 text-center font-semibold text-black"

              >

                Download PDF

              </a>

            )}

            {/* DETAILS */}

            <button

              className="flex-1 bg-white/10 hover:bg-white/20 transition rounded-xl py-3 font-semibold text-white"

            >

              Details

            </button>

          </div>

        </div>

      </div>

    ))}

  </div>

)}

      {/* DOCTOR CHAT */}

      {showMessages && (

        <div className="fixed left-6 bottom-6 w-[400px] bg-[#111111] border border-gray-800 rounded-3xl overflow-hidden shadow-2xl z-50">

          <div className="bg-green-500 text-black px-6 py-4 font-bold text-lg">

            Doctor Conversation

          </div>

          <div className="h-[400px] overflow-y-auto p-4 space-y-4">

            {doctorMessages.map(
              (msg: any) => (

                <div

                  key={msg.id}

                  className={`p-4 rounded-2xl text-sm max-w-[80%] ${
                    msg.sender_id ===
                    JSON.parse(
                      localStorage.getItem(
                        "user"
                      ) || "{}"
                    ).id

                      ? "bg-cyan-500 text-black ml-auto"

                      : "bg-white/10 text-white"

                  }`}

                >

                  {msg.content}

                </div>

              )

            )}

          </div>

          <form

            onSubmit={sendDoctorMessage}

            className="flex border-t border-gray-800"

          >

            <input

              type="text"

              value={messageInput}

              onChange={(e) =>
                setMessageInput(
                  e.target.value
                )
              }

              placeholder="Write a message..."

              className="flex-1 bg-transparent px-4 py-4 outline-none text-white"

            />

            <button

              type="submit"

              className="px-6 text-green-400 font-bold"

            >

              Send

            </button>

          </form>

        </div>

      )}

      {/* AI CHAT */}

      {showChat && (

        <div className="fixed bottom-32 right-6 w-[420px] h-[650px] bg-[#111111] border border-gray-800 rounded-3xl flex flex-col overflow-hidden shadow-2xl z-40">

          <div className="bg-cyan-500 text-black p-5 flex items-center justify-between">

            <div className="flex items-center gap-3">

              <Bot size={28} />

              <div>

                <h2 className="font-bold text-lg">

                  Medical AI Assistant

                </h2>

                <p className="text-sm">

                  Powered by Ollama Mistral

                </p>

              </div>

            </div>

            <button

              onClick={() =>
                setShowChat(false)
              }

              className="bg-black/20 hover:bg-black/40 transition px-3 py-1 rounded-xl"

            >

              ✕

            </button>

          </div>

          <div className="flex-1 overflow-y-auto p-5 space-y-4">

            {chatMessages.length === 0 && (

              <div className="text-center text-gray-500 mt-10">

                <MessageSquare
                  size={50}
                  className="mx-auto mb-4"
                />

                Ask medical questions...

              </div>

            )}

            {chatMessages.map(
              (msg, index) => (

                <div

                  key={index}

                  className={`flex ${
                    msg.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}

                >

                  <div

                    className={`max-w-[80%] rounded-3xl px-5 py-4 ${
                      msg.role === "user"

                        ? "bg-cyan-500 text-black"

                        : "bg-black border border-gray-700 text-white"
                    }`}

                  >

                    {msg.content}

                  </div>

                </div>

              )

            )}

            {chatLoading && (

              <div className="bg-black border border-gray-700 rounded-3xl px-5 py-4 w-fit">

                AI is typing...

              </div>

            )}

          </div>

          <div className="p-4 border-t border-gray-800 flex gap-3">

            <input

              type="text"

              placeholder="Ask medical question..."

              value={chatInput}

              onChange={(e) =>
                setChatInput(
                  e.target.value
                )
              }

              onKeyDown={(e) => {

                if (e.key === "Enter") {

                  handleSendMessage();

                }

              }}

              className="flex-1 bg-black border border-gray-700 rounded-2xl px-4 py-3 outline-none"

            />

            <button

              onClick={
                handleSendMessage
              }

              disabled={chatLoading}

              className="bg-cyan-500 hover:bg-cyan-400 transition rounded-2xl px-5"

            >

              <Send size={20} color="black" />

            </button>

          </div>

        </div>

      )}

      {/* FLOATING BUTTON */}

      <button

        onClick={() =>
          setShowChat(!showChat)
        }

        className="fixed bottom-6 right-6 bg-cyan-500 hover:bg-cyan-400 transition w-16 h-16 rounded-full flex items-center justify-center shadow-2xl z-50"

      >

        <Bot size={32} color="black" />

      </button>

    </main>

  );

}