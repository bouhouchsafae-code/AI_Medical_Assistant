"use client";

import { useState } from "react";

import axios from "axios";

import { useRouter } from "next/navigation";

export default function ChangePasswordPage() {

  const router = useRouter();

  const [password, setPassword] = useState("");

  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // =========================
  // 🔐 UPDATE PASSWORD
  // =========================

  const handleChangePassword = async (

    e: React.FormEvent

  ) => {

    e.preventDefault();

    setError("");

    // =========================
    // ❌ PASSWORD MISMATCH
    // =========================

    if (password !== confirmPassword) {

      setError(

        "Passwords do not match"

      );

      return;

    }

    try {

      setLoading(true);

      const token = localStorage.getItem(

        "token"

      );

      await axios.post(

        "http://127.0.0.1:8000/change-password",

        {

          new_password: password

        },

        {

          headers: {

            Authorization:

              `Bearer ${token}`

          }

        }

      );

      // =========================
      // ✅ UPDATE LOCAL USER
      // =========================

      const user = JSON.parse(

        localStorage.getItem("user") || "{}"

      );

      user.must_change_password = false;

      localStorage.setItem(

        "user",

        JSON.stringify(user)

      );

      // =========================
      // 🚀 REDIRECT
      // =========================

      router.push("/patient-dashboard");

    }

    catch (err) {

      console.log(err);

      setError(

        "Failed to update password"

      );

    }

    finally {

      setLoading(false);

    }

  };

  return (

    <main className="min-h-screen bg-black flex items-center justify-center p-6">

      <div className="w-full max-w-md bg-white/5 border border-white/10 rounded-3xl p-10 text-white">

        <h1 className="text-4xl font-bold mb-4 text-center">

          Change Password

        </h1>

        <p className="text-gray-400 text-center mb-8">

          You must change your password
          before continuing.

        </p>

        {/* Error */}

        {error && (

          <div className="bg-red-500/20 border border-red-500 text-red-300 rounded-xl p-3 mb-6 text-sm">

            {error}

          </div>

        )}

        {/* Form */}

        <form

          onSubmit={handleChangePassword}

          className="space-y-5"

        >

          {/* Password */}

          <div>

            <label className="block mb-2 text-sm text-gray-300">

              New Password

            </label>

            <input

              type="password"

              value={password}

              onChange={(e) =>

                setPassword(e.target.value)

              }

              required

              className="w-full bg-black border border-white/10 rounded-2xl px-4 py-3 outline-none focus:border-cyan-400"

              placeholder="********"

            />

          </div>

          {/* Confirm */}

          <div>

            <label className="block mb-2 text-sm text-gray-300">

              Confirm Password

            </label>

            <input

              type="password"

              value={confirmPassword}

              onChange={(e) =>

                setConfirmPassword(e.target.value)

              }

              required

              className="w-full bg-black border border-white/10 rounded-2xl px-4 py-3 outline-none focus:border-cyan-400"

              placeholder="********"

            />

          </div>

          {/* Button */}

          <button

            type="submit"

            disabled={loading}

            className="w-full bg-cyan-500 hover:bg-cyan-400 transition-all rounded-2xl py-3 font-semibold text-black"

          >

            {

              loading

                ? "Updating..."

                : "Change Password"

            }

          </button>

        </form>

      </div>

    </main>

  );

}