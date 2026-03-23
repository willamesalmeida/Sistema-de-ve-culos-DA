# 🚛 Sistema de Veículos — DA Distribuidora Arapiraca

Sistema interno de consulta e cadastro de motoristas e veículos, desenvolvido para uso exclusivo da **DA Distribuidora Arapiraca**.

---

## 📋 Sobre o Sistema

O sistema permite:

- Cadastrar motoristas e veículos com todos os dados relevantes
- Consultar o motorista responsável por um veículo através da placa
- Validar placas nos padrões **antigo (ABC-1234)** e **Mercosul (ABC1D23)**
- Funcionar 100% offline, sem necessidade de internet

---

## 🖥️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.12+ | Linguagem principal |
| PySide6 | 6.x | Interface gráfica desktop |
| SQLite | — | Banco de dados local |
| QtAwesome | — | Ícones da interface |
| Pillow | — | Manipulação de imagens |
| PyInstaller | — | Empacotamento em .exe |

---

## 📁 Estrutura do Projeto
```
SistemaVeiculos/
├── app/
│   ├── assets/
│   │   ├── images/        ← logo e imagens
│   │   └── photos/        ← fotos dos motoristas
│   ├── core/
│   │   ├── database.py          ← conexão e migrations
│   │   ├── plate_validator.py   ← validação de placas
│   │   ├── drivers_repository.py
│   │   └── vehicles_repository.py
│   ├── data/
│   │   └── fleet.db       ← banco de dados (gerado automaticamente)
│   └── ui/
│       ├── components/
│       │   └── message_dialog.py
│       ├── main_window.py
│       └── register_screen.py
├── main.py
└── requirements.txt
```

---

## 🚀 Como Executar

### Requisitos
- Python 3.12 ou superior
- Windows 10 ou superior

### Instalação

**1. Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/SistemaVeiculos.git
cd SistemaVeiculos
```

**2. Crie e ative o ambiente virtual:**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Execute o sistema:**
```bash
python main.py
```

O banco de dados `fleet.db` será criado automaticamente na primeira execução.

---

## 📦 Gerar Instalador

Para gerar o `.exe` e o instalador:
```bash
# Gerar o executável
pyinstaller --onefile --windowed main.py

# O instalador será gerado com Inno Setup
```

---

## 📌 Funcionalidades Previstas

- [x] Cadastro de motoristas e veículos
- [x] Validação de placas (padrão antigo e Mercosul)
- [x] Dialogs estilizados de feedback
- [x] Navegação entre telas
- [ ] Tela de consulta por placa
- [ ] Card estilo CNH com dados do motorista
- [ ] Campo de foto do motorista
- [ ] Geração do instalador `.exe`

---

## ⚖️ Licença e Direitos Autorais
```
Copyright (c) 2025 DA Distribuidora Arapiraca
Todos os direitos reservados.

Este software é propriedade exclusiva da DA Distribuidora Arapiraca.
É estritamente proibido copiar, modificar, distribuir ou utilizar
este software, no todo ou em parte, sem autorização prévia e por
escrito da DA Distribuidora Arapiraca.

Este sistema foi desenvolvido para uso interno exclusivo.
Qualquer uso não autorizado estará sujeito às penalidades
previstas na Lei nº 9.610/1998 (Lei de Direitos Autorais)
e demais legislações aplicáveis.
```

---

## 👨‍💻 Desenvolvedor

Desenvolvido por **José Willames de Almeida Barbosa**
TI — DA Distribuidora Arapiraca
Arapiraca, Alagoas — Brasil
