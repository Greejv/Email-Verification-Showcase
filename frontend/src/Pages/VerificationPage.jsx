import { useNavigate, useSearchParams } from "react-router-dom";
import { useState, useEffect } from "react";
import '../Styles/VerificationPage.css'

const VerificationPage = () => {

    const navigate = useNavigate();


    // state variable pre stav overenia emailu ktory odosle server
    const [verificationStatus, setVerificationStatus] = useState("");

    // state variable aby sme vedeli ci uz sme dostali odpoved zo serveru
    const [loading, setLoading] = useState(true)


    // ziskanie tokenu z URL adresy
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token");


    // funkcia pre overenie emailu
    const handleVerification = async() => {

        try {
            // odoslanie tokenu na server
            const response = await fetch("http://localhost:8000/api/verification/verify/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ token }),
            })

            // ak server verifikoval email zmeni sa stav overenia
            if (response.ok) {
                const data = await response.json()
                setVerificationStatus(data.detail)
            }

            else {
                const errorData = await response.json()
                setVerificationStatus("Nastala chyba pri overovaní: " + errorData.detail)
            }

        }

        catch (error) {
            setVerificationStatus("Chyba pri odosielaní tokenu: " + error.message)
        }

        finally {
            setLoading(false)
        }

    }


    // automatické spustenie funkcii pri prvom nacitani stranky
    useEffect(() => {

        if (!token) {
            return navigate("/");
        }

        else
            void handleVerification();

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [token]);


    // obsah stranky
    return (

        <div className="verification-page">

            <h1>
                Email Verification Showcase
            </h1>

            <div className="verification-container">
                <h2 className="subtitle">
                    Stav overenia:
                </h2>

                {/* ak sa este nefetchol token, zobrazi sa toto: */}
                {loading &&
                    <p className="verification-status">
                        Prebieha overovanie...
                    </p>
                }

                {/* ak sa uz fetchol token, zobrazi sa status overenia ktory odoslal server */}
                {!loading &&
                    <p className="verification-status">
                        {verificationStatus}
                    </p>
                }

            </div>
        </div>

    )

}

export default VerificationPage