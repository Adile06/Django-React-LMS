import { useState, useEffect } from "react";
import AkademiBaseHeader from "../partials/AkademiBaseHeader";
import AkademiBaseFooter from "../partials/AkademiBaseFooter";
import { Link } from "react-router-dom";
import apiInstance from "../../utils/axios";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await apiInstance.get(`user/password-reset/${email}/`).then((res) => {
        console.log(res.data);
        setIsLoading(false);
        alert("Şifre Değiştirme Emaili Gönderildi");
      });
    } catch (error) {
      console.log("error: ", error);
      setIsLoading(false);
    }
  };

  return (
    <>
      <AkademiBaseHeader />

      <section
        className="container d-flex flex-column vh-100"
        style={{ marginTop: "150px" }}
      >
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Şifremi Unuttum</h1>
                  <span>Hesabınıza Erişmenize Yardımcı Olalım</span>
                </div>
                <form
                  className="needs-validation"
                  noValidate=""
                  onSubmit={handleEmailSubmit}
                >
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                      Email Addresiniz
                    </label>
                    <input
                      type="email"
                      id="email"
                      className="form-control"
                      name="email"
                      placeholder="ornek@xyz.com"
                      required
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>

                  <div>
                    <div className="d-grid">
                      {isLoading === true && (
                        <button disabled type="submit" className="btn btn-primary">
                          İşlem Yapılıyor <i className="fas fa-spinner fa-spin"></i>
                        </button>
                      )}

                      {isLoading === false && (
                        <button type="submit" className="btn btn-primary">
                          Şifre Oluştur <i className="fas fa-arrow-right"></i>
                        </button>
                      )}
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <AkademiBaseFooter />
    </>
  );
}

export default ForgotPassword;
