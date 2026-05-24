"use client";

import {
  useEffect,
  useState,
  useRef
} from "react";

import { useRouter } from "next/navigation";

import axios from "axios";

import { motion } from "framer-motion";


import {
  Activity,
  BrainCircuit,
  FileText,
  Users,
  LogOut,
  UserPlus,
  Search,
  Eye,
  Send,
  Bot,
  MessageSquare
} from "lucide-react";

export default function Dashboard() {

  // =========================
  // ROUTER
  // =========================

  const router = useRouter();

  // =========================
  // PDF REF
  // =========================

  

  // =========================
  // STATS
  // =========================

  const [stats, setStats] = useState({

    total_patients: 0,

    reports_generated: 0,

    pneumonia_cases: 0

  });

  // =========================
  // HISTORY
  // =========================
  

  const [history, setHistory] =
    useState<any[]>([]);

  const [patients, setPatients] =
    useState<any[]>([]);

  const [selectedPatient, setSelectedPatient] =
    useState("");

  // =========================
  // ANALYSIS STATES
  // =========================

  const fileInputRef =
    useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  const [analysisResult, setAnalysisResult] =
    useState<any>(null);

  const [loadingAnalysis, setLoadingAnalysis] =
    useState(false);
  // =========================
  // ➕ ADD PATIENT STATES
  // =========================
  const [showPatientsModal, setShowPatientsModal] =
  useState(false);

  const [searchPatient, setSearchPatient] =
    useState(""); 

  const [showAddPatient, setShowAddPatient] =
    useState(false);

  const [addingPatient, setAddingPatient] =
    useState(false);

  const [patientForm, setPatientForm] =
    useState({

      username: "",

      first_name: "",

      last_name: "",

      age: "",

      phone: "",

      email: "",

      password: "",


    });
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

const [selectedChatPatient, setSelectedChatPatient] =
  useState<any>(null);

const [doctorMessages, setDoctorMessages] =
  useState<any[]>([]);

const [doctorMessageInput, setDoctorMessageInput] =
  useState("");

const [showDoctorChat, setShowDoctorChat] =
  useState(false);

  // =========================
  // LOGOUT
  // =========================
// =========================
// ➕ ADD PATIENT
// =========================

const handleAddPatient =
  async () => {

    try {

      setAddingPatient(true);

      const token =
        localStorage.getItem(
          "token"
        );

      const response =
        await axios.post(

          "http://127.0.0.1:8000/doctor/add-patient",

          {

            ...patientForm,

            age: Number(
              patientForm.age
            )

          },

          {

            headers: {

              Authorization:
                `Bearer ${token}`

            }

          }

        );

      if (
        response.data.success
      ) {

        alert(
          "Patient added successfully"
        );

        setShowAddPatient(
          false
        );

        // refresh patients

        const patientsResponse =
          await axios.get(

            "http://127.0.0.1:8000/doctor/patients",

            {

              headers: {

                Authorization:
                  `Bearer ${token}`

              }

            }

          );

        setPatients(

          patientsResponse
            .data.patients || []

        );

        // reset form

        setPatientForm({

          username: "",

          first_name: "",

          last_name: "",

          age: "",

          phone: "",

          email: "",

          password: "",


        });

      }

    }

    catch (error) {

      console.log(error);

      alert(
        "Failed to add patient"
      );

    }

    finally {

      setAddingPatient(
        false
      );

    }

};
// =========================
// 💬 LOAD CONVERSATION
// =========================

const loadConversation =
  async (patient: any) => {

    try {

      setSelectedChatPatient(
        patient
      );

      setShowDoctorChat(true);

      const token =
        localStorage.getItem(
          "token"
        );

      const response =
        await axios.get(

          `http://127.0.0.1:8000/messages/${patient.id}`,

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

const sendDoctorMessage =
  async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    if (
      !doctorMessageInput.trim()
    ) return;

    try {

      const token =
        localStorage.getItem(
          "token"
        );

      await axios.post(

        "http://127.0.0.1:8000/send-message",

        {

          receiver_id:
            selectedChatPatient.id,

          content:
            doctorMessageInput

        },

        {

          headers: {

            Authorization:
              `Bearer ${token}`

          }

        }

      );

      setDoctorMessageInput(
        ""
      );

      loadConversation(
        selectedChatPatient
      );

    }

    catch (err) {

      console.log(err);

    }

};
// =========================
// 🤖 SEND AI MESSAGE
// =========================

const handleSendMessage =
  async () => {

    if (!chatInput.trim()) return;

    const messageToSend =
      chatInput;

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

      const response =
        await axios.post(

          "http://127.0.0.1:8000/ai/chat",

          {

            message: messageToSend

          }

        );

      const aiMessage = {

        role: "assistant",

        content:
          response.data.response

      };

      setChatMessages((prev) => [

        ...prev,

        aiMessage

      ]);

    }

    catch (error) {

      console.log(error);

    }

    finally {

      setChatLoading(false);

      setChatInput("");

    }

};
  const handleLogout = () => {

    localStorage.removeItem(
      "token"
    );

    router.push("/");

  };

  // =========================
  // DOWNLOAD PDF
  // =========================

const downloadPDF = async () => {

  if (!analysisResult) return;

  try {

    const response =
      await axios.post(

        "http://127.0.0.1:8000/generate-pdf",

        {

          report:
            analysisResult.report

        },

        {

          responseType: "blob"

        }

      );

    // =========================
    // 📄 DOWNLOAD FILE
    // =========================

    const url =
      window.URL.createObjectURL(

        new Blob([response.data])

      );

    const link =
      document.createElement("a");

    link.href = url;

    link.setAttribute(

      "download",

      "medical_report.pdf"

    );

    document.body.appendChild(
      link
    );

    link.click();

    link.remove();

  }

  catch (error) {

    console.log(error);

    alert(
      "Failed to generate PDF"
    );

  }

};

  // =========================
  // LOAD DATA
  // =========================

  useEffect(() => {

    const token =
      localStorage.getItem(
        "token"
      );

    if (!token) {

      router.push("/");

      return;

    }

    // =========================
    // FETCH STATS
    // =========================

    const fetchStats =
      async () => {

        try {

          const response =
            await axios.get(

              "http://127.0.0.1:8000/doctor/dashboard/stats",

              {

                headers: {

                  Authorization:
                    `Bearer ${token}`

                }

              }

            );

          setStats(

        response.data.stats || {

            total_patients: 0,

            reports_generated: 0,

            pneumonia_cases: 0

        }

        );
        }

        catch (error) {

          console.log(error);

        }

      };

    // =========================
    // FETCH HISTORY
    // =========================

    const fetchHistory =
      async () => {

        try {

          const response =
            await axios.get(

              "http://127.0.0.1:8000/analyses/history",

              {

                headers: {

                  Authorization:
                    `Bearer ${token}`

                }

              }

            );

          setHistory(
            response.data.analyses || []
          );

        }

        catch (error) {

          console.log(error);

        }

      };
      const fetchPatients =
  async () => {

    try {

      const response =
        await axios.get(

          "http://127.0.0.1:8000/doctor/patients",

          {

            headers: {

              Authorization:
                `Bearer ${token}`

            }

          }

        );

      setPatients(
        response.data.patients || []
      );

    }

    catch (error) {

      console.log(error);

    }

};
    fetchPatients();
    fetchStats();

    fetchHistory();

    

  }, [router]);

  // =========================
// ANALYZE IMAGE
// =========================

const analyzeImage =
  async (
    file: File
  ) => {

    try {

      setLoadingAnalysis(
        true
      );

      const token =
        localStorage.getItem(
          "token"
        );

      if (!token) {

        router.push("/");

        return;

      }

      // =========================
      // VALIDATE PATIENT
      // =========================

      if (!selectedPatient) {

        alert(
          "Please select a patient"
        );

        return;

      }

      // =========================
      // FORM DATA
      // =========================

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      

      // =========================
      // API CALL
      // =========================

      const response =
      await axios.post(

        `http://127.0.0.1:8000/analyze?patient_id=${selectedPatient}`,

        formData,

        {

          headers: {

            Authorization:
              `Bearer ${token}`,

            "Content-Type":
              "multipart/form-data"

          }

        }

      );

      // =========================
      // SAVE RESULT
      // =========================

      setAnalysisResult(
        response.data
      );

      // =========================
      // REFRESH HISTORY
      // =========================

      const historyResponse =
        await axios.get(

          "http://127.0.0.1:8000/analyses/history",

          {

            headers: {

              Authorization:
                `Bearer ${token}`

            }

          }

        );

      setHistory(

        historyResponse
          .data.analyses

      );

    }

    catch (error) {

      console.log(error);

      alert(
        "Analysis failed"
      );

    }

    finally {

      setLoadingAnalysis(
        false
      );

    }

};

  return (

    <main className="min-h-screen bg-black text-white p-10">

      {/* Header */}
      <div className="flex items-center justify-between mb-10">

        <div>

          <h1 className="text-4xl font-bold">
            Doctor Dashboard
          </h1>

          <p className="text-gray-300 mt-2">
            AI Medical Diagnostic Platform
          </p>

        </div>

        <div className="flex items-center gap-4">

          {/* Logo */}
          <div className="bg-cyan-500 p-4 rounded-2xl">

            <BrainCircuit size={32} />

          </div>
          {/* Patients */}
<button

  onClick={() =>
    setShowPatientsModal(true)
  }

  className="bg-cyan-500 hover:bg-cyan-400 transition px-6 py-4 rounded-2xl flex items-center gap-3 font-semibold text-black"

>

  <Users size={22} />

  Patients

</button>

          {/* Logout */}
          <button

            onClick={handleLogout}

            className="bg-red-500 hover:bg-red-400 transition p-4 rounded-2xl"

          >

            <LogOut size={24} />

          </button>

        </div>

      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

        {/* Patients */}
        <motion.div

          whileHover={{
            scale: 1.03
          }}

          className="bg-[#111111] border border-gray-800 rounded-3xl p-6"

        >

          <div className="flex items-center justify-between mb-4">

            <Users className="text-cyan-400" />

            <span className="text-3xl font-bold">

              {stats.total_patients}

            </span>

          </div>

          <h2 className="text-lg font-semibold">
            Total Patients
          </h2>

        </motion.div>
        

        {/* Reports */}
        <motion.div

          whileHover={{
            scale: 1.03
          }}

          className="bg-[#111111] border border-gray-800 rounded-3xl p-6"

        >

          <div className="flex items-center justify-between mb-4">

            <FileText className="text-green-400" />

            <span className="text-3xl font-bold">

              {stats.reports_generated}

            </span>

          </div>

          <h2 className="text-lg font-semibold">
            Reports Generated
          </h2>

        </motion.div>

        {/* Pneumonia */}
        <motion.div

          whileHover={{
            scale: 1.03
          }}

          className="bg-[#111111] border border-gray-800 rounded-3xl p-6"

        >

          <div className="flex items-center justify-between mb-4">

            <Activity className="text-red-400" />

            <span className="text-3xl font-bold">

              {stats.pneumonia_cases}

            </span>

          </div>

          <h2 className="text-lg font-semibold">
            Pneumonia Cases
          </h2>

        </motion.div>

      </div>
      <div className="mb-6">

  <label className="block mb-2 text-gray-300">

    Select Patient

  </label>

  <select

    value={selectedPatient}

    onChange={(e) =>

      setSelectedPatient(
        e.target.value
      )

    }

    className="w-full bg-black border border-white/10 rounded-2xl p-4"

  >

    <option value="">
      Choose Patient
    </option>

    {patients.map((patient) => (

      <option

        key={patient.id}

        value={patient.id}

      >

        {patient.first_name}
        {" "}
        {patient.last_name}

      </option>

    ))}

  </select>

</div>

      {/* Upload */}
      <div className="bg-[#111111] border border-gray-800 rounded-3xl p-10">

        <h2 className="text-2xl font-bold mb-4">
          Upload X-Ray
        </h2>

        <p className="text-gray-300 mb-6">
          Upload chest X-ray image for AI analysis
        </p>

        <div

          onClick={() =>
            fileInputRef.current?.click()
          }

          className="border-2 border-dashed border-cyan-500 rounded-3xl p-20 text-center cursor-pointer hover:border-cyan-400 transition"

        >

          {/* Hidden Input */}
          <input

            type="file"

            accept="image/*"

            hidden

            ref={fileInputRef}

            onChange={async (e) => {

              if (
                e.target.files?.[0]
              ) {

                const file =
                  e.target.files[0];

                setSelectedFile(
                  file
                );

                await analyzeImage(
                  file
                );

              }

            }}

          />

          {/* Default */}
          {!selectedFile &&
            !loadingAnalysis && (

            <p className="text-gray-300 text-lg">

              Drag & Drop X-ray Image Here
              <br />
              or Click to Upload

            </p>

          )}

          {/* Loading */}
          {loadingAnalysis && (

            <p className="text-cyan-400 text-lg animate-pulse">

              AI Analyzing Image...

            </p>

          )}

          {/* Uploaded */}
          {selectedFile &&
            !loadingAnalysis && (

            <div>

              <p className="text-green-400 text-lg font-semibold">

                Image Uploaded Successfully

              </p>

              <p className="text-gray-300 mt-2">

                {selectedFile.name}

              </p>

            </div>

          )}

        </div>

      </div>

      {/* Analysis Result */}
{analysisResult && (

  <div

    className="mt-10 bg-[#111111] border border-gray-800 rounded-3xl p-10"

  >

    <h2 className="text-3xl font-bold mb-8">
      Multi-Disease AI Analysis
    </h2>

    {/* ========================= */}
    {/* 🖼️ ORIGINAL IMAGE */}
    {/* ========================= */}

    <div className="mb-10">

      <h3 className="text-xl font-bold mb-4">
        Original Chest X-Ray
      </h3>

      <img

        src={analysisResult.image_url}

        alt="xray"

        crossOrigin="anonymous"

        className="rounded-2xl w-full md:w-[500px]"

      />

    </div>

    {/* ========================= */}
    {/* 🔥 MULTI HEATMAPS */}
    {/* ========================= */}

    <div>

      <h3 className="text-2xl font-bold mb-6">
        Disease Heatmaps
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

        {analysisResult.heatmaps?.map(

          (item: any, index: number) => (

            <div

              key={index}

              className="bg-black rounded-2xl p-6"

            >

              <h4 className="text-2xl font-bold mb-3">

                {item.disease}

              </h4>

              <p className="text-cyan-400 mb-4">

                AI Detected Region

              </p>

              <img

                src={item.url}

                alt={item.disease}

                crossOrigin="anonymous"

                className="rounded-2xl"

              />

            </div>

          )

        )}

      </div>

    </div>

    {/* ========================= */}
    {/* 📄 REPORT */}
    {/* ========================= */}

    <div className="mt-10">

      <h3 className="text-2xl font-bold mb-4">
        Medical Report
      </h3>

      <div className="bg-black rounded-2xl p-6 whitespace-pre-wrap text-gray-300">

        {analysisResult.report}

      </div>

      {/* ========================= */}
      {/* 📥 PDF */}
      {/* ========================= */}

      <button

        onClick={downloadPDF}

        className="mt-6 bg-cyan-500 hover:bg-cyan-400 transition px-6 py-3 rounded-xl font-semibold"

      >

        Download PDF Report

      </button>

    </div>

  </div>

)}

      {/* History */}
      <div className="mt-10">

        <h2 className="text-3xl font-bold mb-6">
          Recent Analyses
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {history.map((item) => (

            <motion.div

              key={item.id}

              whileHover={{
                scale: 1.02
              }}

              className="bg-[#111111] border border-gray-800 rounded-3xl p-6"

            >

              {/* Images */}
              <div className="grid grid-cols-2 gap-4 mb-6">

                {/* Xray */}
                <div>

                  <p className="text-sm text-gray-300 mb-2">
                    X-Ray
                  </p>

                  {item.image_url?.startsWith(
                    "http"
                  ) && (

                    <img

                      src={item.image_url}

                      alt="xray"

                      className="rounded-2xl h-52 w-full object-cover"

                    />

                  )}

                </div>

                {/* Heatmap */}
                <div>

                  <p className="text-sm text-gray-300 mb-2">
                    Heatmap
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">

                    {item.heatmaps?.map(

                      (heatmap: any, idx: number) => (

                        <div

                          key={idx}

                          className="bg-black rounded-2xl p-4"

                        >

                          <h4 className="text-lg font-bold mb-3">

                            {heatmap.disease}

                          </h4>

                          <img

                            src={heatmap.url}

                            alt={heatmap.disease}

                            crossOrigin="anonymous"

                            className="rounded-xl"

                          />

                        </div>

                      )

                    )}

                  </div>


                </div>

              </div>

              {/* Infos */}
              <div className="space-y-2">

                <div className="flex justify-between">

                  <span className="text-gray-300">
                    Diagnosis
                  </span>

                  <span className="font-semibold">

                    {item.diagnosis}

                  </span>

                </div>

                <div className="flex justify-between">

                  <span className="text-gray-300">
                    Confidence
                  </span>

                  <span className="font-semibold">

                    {(item.confidence * 100).toFixed(0)}%

                  </span>

                </div>

                <div className="flex justify-between">

                  <span className="text-gray-300">
                    Patient
                  </span>

                  <span className="font-semibold">

                    {item.patient.first_name}
                    {" "}
                    {item.patient.last_name}

                  </span>

                </div>

                <div className="flex justify-between">

                  <span className="text-gray-300">
                    Date
                  </span>

                  <span className="font-semibold">

                    {new Date(
                      item.created_at
                    ).toLocaleString()}

                  </span>

                </div>

              </div>

            </motion.div>

          ))}

        </div>

      </div>

      {/* =========================
➕ ADD PATIENT MODAL
========================= */}

{
  showAddPatient && (

    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">

      <div className="bg-[#111111] border border-gray-800 rounded-3xl p-8 w-full max-w-xl">

        <h2 className="text-3xl font-bold mb-6">
          Add New Patient
        </h2>

        <div className="grid grid-cols-2 gap-4">

          <input
            placeholder="Username"
            value={patientForm.username}
            onChange={(e) =>
              setPatientForm({
                ...patientForm,
                username: e.target.value
              })
            }
            className="bg-black border border-gray-700 rounded-2xl p-4"
          />

          <input
            placeholder="First Name"
            value={patientForm.first_name}
            onChange={(e) =>
              setPatientForm({
                ...patientForm,
                first_name: e.target.value
              })
            }
            className="bg-black border border-gray-700 rounded-2xl p-4"
          />

          <input
            placeholder="Last Name"
            value={patientForm.last_name}
            onChange={(e) =>
              setPatientForm({
                ...patientForm,
                last_name: e.target.value
              })
            }
            className="bg-black border border-gray-700 rounded-2xl p-4"
          />

          <input
            type="number"
            placeholder="Age"
            value={patientForm.age}
            onChange={(e) =>
              setPatientForm({
                ...patientForm,
                age: e.target.value
              })
            }
            className="bg-black border border-gray-700 rounded-2xl p-4"
          />

          <input
            placeholder="Phone"
            value={patientForm.phone}
            onChange={(e) =>
              setPatientForm({
                ...patientForm,
                phone: e.target.value
              })
            }
            className="bg-black border border-gray-700 rounded-2xl p-4"
          />

          

        </div>

        <input
          placeholder="Email"
          value={patientForm.email}
          onChange={(e) =>
            setPatientForm({
              ...patientForm,
              email: e.target.value
            })
          }
          className="bg-black border border-gray-700 rounded-2xl p-4 mt-4 w-full"
        />

        <input
          type="password"
          placeholder="Temporary Password"
          value={patientForm.password}
          onChange={(e) =>
            setPatientForm({
              ...patientForm,
              password: e.target.value
            })
          }
          className="bg-black border border-gray-700 rounded-2xl p-4 mt-4 w-full"
        />

        <div className="flex justify-end gap-4 mt-6">

          <button

            onClick={() =>
              setShowAddPatient(
                false
              )
            }

            className="bg-gray-700 hover:bg-gray-600 transition px-5 py-3 rounded-2xl"

          >
            Cancel
          </button>

          <button

            onClick={
              handleAddPatient
            }

            disabled={
              addingPatient
            }

            className="bg-cyan-500 hover:bg-cyan-400 transition px-5 py-3 rounded-2xl text-black font-semibold"

          >

            {
              addingPatient
                ? "Adding..."
                : "Add Patient"
            }

          </button>

        </div>

      </div>

    </div>

  )
}
{/* =========================
👥 PATIENTS MODAL
========================= */}

{
  showPatientsModal && (

    <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center">

      <div className="bg-[#111111] border border-gray-800 rounded-3xl w-full max-w-5xl p-8 max-h-[90vh] overflow-y-auto">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">

          <h2 className="text-3xl font-bold">

            Patients

          </h2>

          <button

            onClick={() =>
              setShowPatientsModal(false)
            }

            className="bg-red-500 hover:bg-red-400 transition px-5 py-2 rounded-2xl"

          >

            Close

          </button>

        </div>

        {/* Search + Add */}
        <div className="flex gap-4 mb-8">

          <div className="flex-1 relative">

            <Search
              className="absolute left-4 top-4 text-gray-500"
              size={20}
            />

            <input

              type="text"

              placeholder="Search patient by first name..."

              value={searchPatient}

              onChange={(e) =>
                setSearchPatient(
                  e.target.value
                )
              }

              className="w-full bg-black border border-gray-700 rounded-2xl pl-12 pr-4 py-4"

            />

          </div>

          <button

            onClick={() => {

              setShowPatientsModal(false);

              setShowAddPatient(true);

            }}

            className="bg-cyan-500 hover:bg-cyan-400 transition px-6 rounded-2xl text-black font-semibold flex items-center gap-2"

          >

            <UserPlus size={20} />

            Add Patient

          </button>

        </div>

        {/* Patients List */}
        <div className="space-y-4">

          {
            patients

              .filter((patient) =>

                patient.first_name
                  ?.toLowerCase()
                  .includes(
                    searchPatient.toLowerCase()
                  )

              )

              .sort((a, b) =>

                a.patient_number.localeCompare(
                  b.patient_number
                )

              )

              .map((patient) => (

                <div

                  key={patient.id}

                  className="bg-black border border-gray-800 rounded-2xl p-5 flex items-center justify-between"

                >

                  <div>

                    <div className="text-cyan-400 font-semibold">

                      {patient.patient_number}

                    </div>

                    <div className="text-xl font-bold">

                      {patient.first_name} {patient.last_name}

                    </div>

                    <div className="text-gray-400">

                      {patient.email}

                    </div>

                  </div>

                  <button

                    onClick={() =>

                      router.push(

                        `/dashboard/patient/${patient.id}`

                      )

                    }

                    className="bg-cyan-500 hover:bg-cyan-400 transition px-5 py-3 rounded-2xl text-black font-semibold flex items-center gap-2"

                  >

                    <Eye size={18} />

                    Details

                  </button>
                  <button

                    onClick={() =>
                      loadConversation(
                        patient
                      )
                    }

                    className="bg-green-500 hover:bg-green-400 transition p-3 rounded-xl"

                  >

                    <MessageSquare
                      size={18}
                      className="text-black"
                    />

                  </button>

                </div>

              ))
          }

        </div>

      </div>

    </div>

  )
}
{/* =========================
🤖 CHAT BUTTON
========================= */}

<button

  onClick={() =>
    setShowChat(!showChat)
  }

  className="fixed bottom-6 right-6 bg-cyan-500 hover:bg-cyan-400 transition w-20 h-20 rounded-full flex items-center justify-center shadow-2xl z-50"

>

  <Bot size={35} color="black" />

</button>

{/* =========================
🤖 AI CHAT
========================= */}

{
  showChat && (

    <div className="fixed bottom-32 right-6 w-[420px] h-[650px] bg-[#111111] border border-gray-800 rounded-3xl flex flex-col overflow-hidden shadow-2xl z-40">

      {/* Header */}
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

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4">

        {
          chatMessages.length === 0 && (

            <div className="text-center text-gray-500 mt-10">

              <MessageSquare
                size={50}
                className="mx-auto mb-4"
              />

              Ask medical questions...

            </div>

          )
        }

        {
          chatMessages.map(

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

          )
        }

        {
          chatLoading && (

            <div className="bg-black border border-gray-700 rounded-3xl px-5 py-4 w-fit">

              AI is typing...

            </div>

          )
        }

      </div>

      {/* Input */}
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

  )
}
{/* ========================= */}
{/* 💬 DOCTOR CHAT WINDOW */}
{/* ========================= */}

{showDoctorChat && (

  <div className="fixed right-6 bottom-6 w-[420px] bg-[#111111] border border-gray-800 rounded-3xl overflow-hidden shadow-2xl z-50">

    {/* Header */}

    <div className="bg-green-500 text-black px-6 py-4 flex items-center justify-between">

      <div>

        <h2 className="font-bold text-lg">

          {
            selectedChatPatient
              ?.first_name
          }

        </h2>

        <p className="text-sm">

          Patient Conversation

        </p>

      </div>

      <button

        onClick={() =>
          setShowDoctorChat(
            false
          )
        }

        className="text-black text-xl"

      >

        ✕

      </button>

    </div>

    {/* Messages */}

    <div className="h-[450px] overflow-y-auto p-4 space-y-4">

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

    {/* Input */}

    <form

      onSubmit={
        sendDoctorMessage
      }

      className="flex border-t border-gray-800"

    >

      <input

        type="text"

        value={
          doctorMessageInput
        }

        onChange={(e) =>
          setDoctorMessageInput(
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

    </main>

  );

}