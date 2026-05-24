"use client";

import { useState } from "react";

import axios from "axios";

import { useRouter } from "next/navigation";

export default function LoginPage() {

  const router = useRouter();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // =========================
  // 🔐 LOGIN
  // =========================

  const handleLogin = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    setLoading(true);

    setError("");

    try {

      const response = await axios.post(

        "http://127.0.0.1:8000/login",

        {
          email: email,
          password: password
        }

      );

      // =========================
      // ✅ SUCCESS
      // =========================

      if (response.data.success) {

        // save token
        localStorage.setItem(
          "token",
          response.data.access_token
        );

        // save user
        localStorage.setItem(
          "user",
          JSON.stringify(
            response.data.user
          )
        );

        // redirect dashboard
        if (

          response.data.user
            .must_change_password

        ) {

          router.push(

            "/change-password"

          );

        }

        else {

          if (

            response.data.user.role
              === "doctor"

          ) {

            router.push(

              "/dashboard"

            );

          }

          else {

            router.push(

              "/patient-dashboard"

            );

          }

        }

      }

      else {

        setError(
          response.data.message
        );

      }

    }

    catch (err: any) {

      console.log(err);

      setError(
        "Invalid email or password"
      );

    }

    finally {

      setLoading(false);

    }

  };

  return (

    <main className="min-h-screen bg-black flex items-center justify-center p-6">

      <div className="w-full max-w-md bg-white/5 border border-white/10 rounded-3xl p-10 text-white">

        {/* Title */}
        <div className="mb-8 text-center">

          <h1 className="text-4xl font-bold mb-2">
            AI Medical Assistant
          </h1>

          <p className="text-gray-400">
            Login to continue
          </p>

        </div>

        {/* Error */}
        {
          error && (
            <div className="bg-red-500/20 border border-red-500 text-red-300 rounded-xl p-3 mb-6 text-sm">
              {error}
            </div>
          )
        }

        {/* Form */}
        <form
          onSubmit={handleLogin}
          className="space-y-5"
        >

          {/* Email */}
          <div>

            <label className="block mb-2 text-sm text-gray-300">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
              required
              className="w-full bg-black border border-white/10 rounded-2xl px-4 py-3 outline-none focus:border-cyan-400"
              placeholder="doctor@gmail.com"
            />

          </div>

          {/* Password */}
          <div>

            <label className="block mb-2 text-sm text-gray-300">
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              required
              className="w-full bg-black border border-white/10 rounded-2xl px-4 py-3 outline-none focus:border-cyan-400"
              placeholder="******"
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
                ? "Loading..."
                : "Login"
            }
          </button>

        </form>

      </div>

    </main>

  );
}