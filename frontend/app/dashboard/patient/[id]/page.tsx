"use client";

import axios from "axios";

import { useEffect, useState } from "react";

import { useParams, useRouter } from "next/navigation";

import {

  ArrowLeft,

  Download,

  Activity,

  Calendar,

  User,

  Mail,

  Phone

} from "lucide-react";

import { motion } from "framer-motion";

export default function PatientDetailsPage() {

  const params = useParams();

  const router = useRouter();

  const patientId = params.id;

  const [loading, setLoading] =
    useState(true);

  const [patientData, setPatientData] =
    useState<any>(null);

  // =========================
  // 📥 FETCH PATIENT
  // =========================

  useEffect(() => {

    fetchPatient();

  }, []);

  const fetchPatient =
    async () => {

      try {

        const token =
          localStorage.getItem(
            "token"
          );

        const response =
          await axios.get(

            `http://127.0.0.1:8000/doctor/patient/${patientId}`,

            {

              headers: {

                Authorization:
                  `Bearer ${token}`

              }

            }

          );

        setPatientData(
          response.data
        );

      }

      catch (error) {

        console.log(error);

        alert(
          "Failed to load patient"
        );

      }

      finally {

        setLoading(false);

      }

    };

  // =========================
  // ⏳ LOADING
  // =========================

  if (loading) {

    return (

      <div className="min-h-screen bg-black text-white flex items-center justify-center">

        Loading...

      </div>

    );

  }

  const patient =
    patientData?.patient;

  const analyses =
    patientData?.analyses || [];
  
    // =========================
// 📄 DOWNLOAD PDF
// =========================

const downloadPDF = async (

  diagnosis: string,

  confidence: number

) => {

  try {

    const report = `

==============================
      MEDICAL REPORT
==============================

Patient Information

First Name: ${patientData?.patient?.first_name}

Last Name: ${patientData?.patient?.last_name}

Email: ${patientData?.patient?.email}

Phone: ${patientData?.patient?.phone}

Patient Number: ${patientData?.patient?.patient_number}

-----------------------------------

AI Diagnostic Report

Diagnosis: ${diagnosis}

Confidence: ${(confidence * 100).toFixed(1)}%

The AI system analyzed the chest X-ray
and generated this medical report.

-----------------------------------

Doctor Information

Doctor: Dr. ${patientData?.doctor?.first_name} ${patientData?.doctor?.last_name}

Speciality: ${patientData?.doctor?.speciality}

-----------------------------------

⚠️ This system is an AI assistant
and does not replace a doctor.

`;

    const response =
      await axios.post(

        "http://127.0.0.1:8000/generate-pdf",

        {

          report

        },

        {

          responseType: "blob"

        }

      );

    // =========================
    // 📥 DOWNLOAD FILE
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

      `analysis_${diagnosis}.pdf`

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
      "Failed to download PDF"
    );

  }

};

  // =========================
  // 🚀 UI
  // =========================

  return (

    <main className="min-h-screen bg-black text-white p-8">

      {/* Header */}
      <div className="flex items-center justify-between mb-10">

        <div>

          <h1 className="text-5xl font-bold">

            Patient Details

          </h1>

          <p className="text-gray-400 mt-2">

            Medical history & analyses

          </p>

        </div>

        <button

          onClick={() =>
            router.push("/dashboard")
          }

          className="bg-cyan-500 hover:bg-cyan-400 transition px-5 py-4 rounded-2xl flex items-center gap-2 text-black font-semibold"

        >

          <ArrowLeft size={20} />

          Back

        </button>

      </div>

      {/* Patient Info */}
      <div className="bg-[#111111] border border-gray-800 rounded-3xl p-8 mb-10">

        <div className="flex items-center justify-between">

          <div>

            <div className="text-cyan-400 font-semibold mb-2">

              {patient.patient_number}

            </div>

            <h2 className="text-4xl font-bold">

              {patient.first_name} {patient.last_name}

            </h2>

          </div>

          <div className="bg-cyan-500 p-5 rounded-3xl">

            <User size={35} />

          </div>

        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">

          <div className="bg-black rounded-2xl p-5">

            <div className="flex items-center gap-3 text-cyan-400 mb-2">

              <Mail size={18} />

              Email

            </div>

            <p>{patient.email}</p>

          </div>

          <div className="bg-black rounded-2xl p-5">

            <div className="flex items-center gap-3 text-cyan-400 mb-2">

              <Phone size={18} />

              Phone

            </div>

            <p>{patient.phone}</p>

          </div>

          <div className="bg-black rounded-2xl p-5">

            <div className="flex items-center gap-3 text-cyan-400 mb-2">

              <Activity size={18} />

              Age

            </div>

            <p>{patient.age}</p>

          </div>

        </div>

      </div>

      {/* Analyses */}
      <div>

        <h2 className="text-3xl font-bold mb-6">

          Analyses History

        </h2>

        {
          analyses.length === 0 ? (

            <div className="bg-[#111111] border border-gray-800 rounded-3xl p-10 text-center text-gray-400">

              No analyses found

            </div>

          ) : (

            <div className="space-y-8">

              {
                analyses.map(
                  (analysis: any) => (

                    <motion.div

                      key={analysis.id}

                      initial={{
                        opacity: 0,
                        y: 20
                      }}

                      animate={{
                        opacity: 1,
                        y: 0
                      }}

                      className="bg-[#111111] border border-gray-800 rounded-3xl p-8"

                    >

                      {/* Header */}
                      <div className="flex items-center justify-between mb-6">

                        <div>

                          <div className="text-cyan-400 font-semibold">

                            Analysis #{analysis.id}

                          </div>

                          <h3 className="text-3xl font-bold mt-2">

                            {analysis.diagnosis}

                          </h3>

                        </div>

                        <div className="text-right">

                          <div className="text-green-400 text-2xl font-bold">

                            {(analysis.confidence * 100).toFixed(1)}%

                          </div>

                          <div className="text-gray-400 text-sm flex items-center gap-2 justify-end mt-2">

                            <Calendar size={16} />

                            {

                              new Date(
                                analysis.created_at
                              ).toLocaleString()

                            }

                          </div>

                        </div>

                      </div>

                      {/* Images */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                        <div>

                          <p className="mb-3 text-gray-400">

                            X-Ray Image

                          </p>

                          <img

                            src={analysis.image_url}

                            alt="xray"

                            className="rounded-3xl border border-gray-700 w-full"

                          />

                        </div>

                        <div>

                          <p className="mb-3 text-gray-400">

                            Heatmap

                          </p>

                          <img

                            src={analysis.heatmap_url}

                            alt="heatmap"

                            className="rounded-3xl border border-gray-700 w-full"

                          />

                        </div>

                      </div>

                      {/* PDF */}
                      <div className="mt-8">

                      <button

                        onClick={() =>

                        downloadPDF(

                          analysis.diagnosis,

                          analysis.confidence

                        )

                      }

  className="bg-cyan-500 hover:bg-cyan-400 transition px-5 py-3 rounded-2xl flex items-center gap-2 text-black font-semibold"

>

                          <Download size={18} />

                          Download Report PDF

                        </button>

                      </div>

                    </motion.div>

                  )
                )
              }

            </div>

          )
        }

      </div>

    </main>

  );

}