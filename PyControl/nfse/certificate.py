class Certificate:

    @classmethod
    def get_content(cls, text):
        cert_buffer = text.replace("\n", "")
        cert_data = cert_buffer.split("-----BEGIN CERTIFICATE-----")
        cert_buffer = str((cert_data[1].replace("-----END CERTIFICATE-----", "")))
        return cert_buffer
