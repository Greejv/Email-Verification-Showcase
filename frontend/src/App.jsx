import { BrowserRouter, Routes, Route } from "react-router-dom";
import SendEmailPage from "./Pages/SendEmailPage.jsx";
import VerificationPage from "./Pages/VerificationPage.jsx";

const App = () => {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<SendEmailPage />} />
                <Route path="/verify" element={<VerificationPage />} />
            </Routes>
        </BrowserRouter>
    )

}

export default App;