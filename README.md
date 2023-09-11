## General

The `shell2` platform provides AI-powered, unrestricted code + data sandboxes with high CPU & RAM, with minimal configuration. A mix between Code Interpreter & Replit

`shell2-cli` is the official CLI for the [shell2.raiden.ai](https://shell2.raiden.ai) platform - works across **Linux, OS X, Windows**

It allows you to create live sessions, including multiplayer with other users, and run sequences, directly from your terminal.

It also allows you to sync your local files directly with the shell2 sandbox, and receive any created file in real time.

In addition to voice input for sessions (experimental)

---

## Installation

1. Install the CLI as follows
```
pip install -U shell2-cli
```

* *if you  get `ERROR: Could not build wheels for PyAudio, which is required to install pyproject.toml-based projects`, make sure you install pyaudio dependencies first*:
    * on linux, `apt install python3-pyaudio`
    * on OS X, `brew install portaudio`
    
* *if you do not want to use the voice input feature, or if there are audio configuration errors, install a previous version of the cli without voice input* - `pip install shell2-cli==0.105`

2. Setup your shell2 API key by running the command from the terminal


```sh
shell2 --key "YOUR_SHELL2_API_KEY"
```

*(your API key is under settings in [shell2.raiden.ai](https://shell2.raiden.ai) )*

That's all.

*note: before you use `shell2`, make sure you have setup your API keys under settings in [shell2.raiden.ai](https://shell2.raiden.ai) (such as **OpenAI** if you select **GPT** as a model, or other providers like **Replicate**...) - your keys are safely stored and wrapped in 2 encryption layers*


## Usage

The CLI can be used in 2 ways

* 1 . Interactive CLI, which is the easiest way, and most comprehensive
  
  Simply run the following in your terminal (from the folder in which generated data and files will be downloaded) and follow along

    ```sh
    shell2
    ```

* 2 . Using one-line commands described below

---

### Create a new session

Navigate to the folder in which you would like to start - where data and files generated in the `shell2` sandbox will be downloaded in real time - and run the following in your terminal

```sh
shell2 --session
```

The terminal will enter live mode and you'll be able to interact with the sandbox in real time *(and with other users in the multiplayer case)*

You can add the following options
* `--timeout TIMEOUT_IN_SECONDS` : Max timeout for your session (defaults to 600 seconds)
* `--voice` : Use voice input to send messages (experimental)
* `--multiplayer` : Enable multiplayer in your created session. You will be provided with a shareable url for the multiplayer session.
* `--nosync` : By default, the files in your current folder will be uploaded to the session you are trying to create or join (< if 500 Mb total). Use this option to disable it.

*example*
```sh
shell2 --session --timeout 500 --multiplayer
```

### Join a multiplayer session

Users that create multiplayer sessions *(or enable it)* receive a shareable URL.

You can use that url to join a multiplayer session from your terminal, like this

```sh
shell2 --session --url "https://shell2.raiden.ai/view/session/example@raiden.ai/945c846a-5e25-455f-09ba-7e39a5f20d11"
```

The terminal will enter live mode and you'll be able to interact with the sandbox in real time.

You can add the following options when joining a session
* `--voice` : Use voice input to send messages (experimental)
* `--nosync` : By default, the files in your current folder will be uploaded to the session you are trying to create or join (< if 500 Mb total). Use this option to disable it.


---

### Run a sequence

Sequences are a predefined list of messages that run consecutively.

To run a sequence:
* Create a `sequence.txt` file in your current folder.
* Write a list of steps in the text file, separated by an empty line.

  *All the shell2 commands ( described in [shell2.raiden.ai](https://shell2.raiden.ai) docs, and better explained in the webapp sessions ), such as `/doc` , `/web` , `/run` , `/shell` , etc... are available here.*
  
* Run this from your terminal (from the same folder)
  ```sh
  shell2 --sequence
  ```
* *optional* - you can add these options to the command:
    * `--timeout TIMEOUT_IN_SECONDS` : Max timeout for your sequence (defaults to 600 seconds)
    * `--webhook "WEBHOOK_URL"` : Webhook URL to send sequence execution data after completion

  
The terminal will display updates in real time until the sequence closes.

Any generated files will be created in your current folder.

##### Basic Sequence Example

A simple example of `sequence.txt` which would generate a png file in your current folder :

```sh
/doc https://raw.githubusercontent.com/raidendotai/shell2-example-data/main/mlb_2012.csv

plot teams payrolls vs winnings in a png file
```

---

#### Sequences Examples

##### Files sync + sequences = Magic

Since files in your current folder are automatically uploaded to the sandbox *(if total < 500 Mb)* when running a sequence, you can take advantage of the feature like this

* example of `sequence.txt`, in the same folder as `group_photo.jpg`:

    * ```sh
        extract faces from group_photo.jpg, save each face in file under subfolder called extracted_faces
        ```
    * *would generate the extracted_faces/... images directly in your local folder* 

* example of `sequence.txt`, in the same folder as `my_paper.pdf` and `friend_paper.pdf`:

    * ```sh
        /doc my_paper.pdf extract the findings of this paper
        
        /doc friend_paper.pdf extract research findings from this document
        
        /m from data you extracted, create a csv file with a single row "findings" - max 15 words per entry
        ```
    * *would generate a csv file in your local folder*

* example of `sequence.txt`, in the same folder as `my_audio.mp3`:

    * ```sh
        extract the first 10 seconds of my_audio.mp3 and save it in m4a format
        ```
    * *would generate a new m4a in your local folder*

---

for any questions or enquiries, feel free to contact via email or on twitter [@n_raidenai](https://twitter.com/n_raidenai)
