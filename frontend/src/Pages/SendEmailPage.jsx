import { useState } from "react"
import '../Styles/SendEmailPage.css'

const SendEmailPage = () => {

    // state variables
    const [email, setEmail] = useState("")
    const [error, setError] = useState("")


    // ak sa email odosle, nastavi sa true a zobrazí sa okno
    const [sentComplete, setSentComplete] = useState(false)


    // funkcia pre odoslanie emailu
    const handleVerify = async() => {

        try {
            // odoslanie emailu na server
            const response = await fetch("http://localhost:8000/api/verification/send/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email }),
            })

            // ak server spracuje email v poriadku, nastavi sa variable na true a zobrazi sa okno
            if (response.ok) {
                setSentComplete(true)
            }

            // ak nie, nastavi sa error a zobrazi chybu
            else {

                const data = await response.json()
                if (data?.email?.length > 0) {
                    setError("Chyba pri odosielaní Emailu: " + data?.email?.[0])
                }
                else {
                    setError("Chyba pri odosielaní Emailu: " + response.statusText)
                }

            }

        }

        // nastaví sa error ak sa nepodarí odoslať email na server
        catch (error) {
            setError("Nepodarilo sa odoslať Email: " + error.message)
       }

    }


    // obsah stranky
    return (
        <div className="sendemail-page">

            <h1 className="title">
                Email Verification Showcase
            </h1>

            <h2 className="subtitle">
                Overte si Váš Email ⬇
            </h2>

            <div className="email-input-container">
                <input
                    name="email"
                    autoComplete="email"
                    placeholder="Zadajte Váš Email"
                    className="email-input"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <button className="verify-button" onClick={handleVerify}>
                    Odoslať
                </button>
                {error && <p className="error-message">{error}</p>}
            </div>

            {/* okno ktore sa zobrazi ak server odosle email */}
            {sentComplete && <div className="sent-complete-window">
                <p className="sent-complete-text top">
                    Overovací email, bol odoslaný na: <i>{email}</i>
                </p>
                <p className="sent-complete-text bottom">
                    Prosím, skontrolujte si svoj email a kliknite na odkaz pre overenie.
                </p>
            </div> }

        </div>

    )

}


export default SendEmailPage