/*
    MP3 to WAV converter
    (c) 2020 github.com/AlexIII
*/

const dragAndDropArea = document.querySelector(".drag-and-drop-area")
const fileInputElem = document.querySelector("#file-input")
const fileTableBodyElem = document.querySelector("#file-table-body")
const saveButton = document.querySelector("#save-button")
const clearButton = document.querySelector("#clear-button")
const sampleRateInput = document.querySelector("#wav-sample-rate")
const bitDepthInput = document.querySelector("#wav-bit-depth")
const channelsInput = document.querySelector("#wav-channels")
const waitOverlayElem = document.querySelector(".overlay-wait")

const isFirefox = navigator.userAgent.toLowerCase().indexOf("firefox") > -1
document
  .querySelectorAll(".fx-notice")
  .forEach(el => (el.style.display = isFirefox ? "none" : "block"))

// get initial settings from URL hash anchor
// example: index.html#8&mix&32000
if (window.location.hash) {
  const initVals = window.location.hash.substr(1).split("&")
  const bitDepth = ~~initVals[0]
  const channels = initVals[1]
  const sampleRate = ~~initVals[2]
  if (bitDepth === 8 || bitDepth === 16) bitDepthInput.value = String(bitDepth)
  if (
    channels === "both" ||
    channels === "left" ||
    channels === "right" ||
    channels === "mix"
  )
    channelsInput.value = channels
  if (sampleRate >= 8000 || sampleRate <= 64000)
    sampleRateInput.value = String(sampleRate)
}

const waitOverlay = isOn => (
  (waitOverlayElem.style.visibility = isOn ? "visible" : "collapse"), undefined
)

const initDragAndDropArea = (elem, highlightClassName, ondrop) => {
  elem.ondrop = ev => {
    elem.classList.remove(highlightClassName)
    ev.preventDefault()
    if (ev.dataTransfer?.items) {
      const files = Array.from(ev.dataTransfer.items)
        .filter(it => it.kind === "file")
        .map(it => it.getAsFile())
      if (files.length) ondrop(files)
    } else if (ev.dataTransfer?.files) {
      const files = Array.from(ev.dataTransfer?.files)
      if (files.length) ondrop(files)
    }
  }
  elem.ondragover = ev => {
    ev.preventDefault()
  }
  elem.ondragenter = () => elem.classList.add(highlightClassName)
  elem.ondragleave = () => elem.classList.remove(highlightClassName)
}

const initOpenFiles = onopen => {
  initDragAndDropArea(dragAndDropArea, "drag-and-drop-area-highlight", onopen)
  fileInputElem.onchange = () => {
    if (fileInputElem.files) {
      onopen(Array.from(fileInputElem.files))
      fileInputElem.value = ""
    }
  }
}

const makeFileTableRows = (files, playing, stats) =>
  files
    .map(
      (f, idx) => `<tr> 
            <td>${idx + 1}</td> 
            <td>${f.name}</td> 
            <td>${Math.round(stats[idx].duration / 60)}:${Math.round(
        stats[idx].duration % 60
      )}</td> 
            <td>${(stats[idx].inSize / 1024 / 1024).toFixed(1)}Mbyte -> ${(
        stats[idx].outSize /
        1024 /
        1024
      ).toFixed(1)}Mbyte</td> 
            <td onclick="removeFileButtonHandler(${idx});"></td> 
            <td onclick="playPauseButtonHandler(${idx});">${
        idx !== playing ? "&#x23F5" : "&#x23F8"
      }</td> 
        </tr>`
    )
    .join("\n")

class AudioFilesProcessor {
  files = []
  playing = null
  stopPlaying = null

  constructor() {
    globalThis["removeFileButtonHandler"] = this.remove.bind(this)
    globalThis["playPauseButtonHandler"] = this.playPause.bind(this)
    saveButton.onclick = async () => {
      if (!this.files.length) return
      waitOverlay(true)
      await Promise.all(
        this.files.map(f =>
          this.convertAndSaveAudioBuffer(
            f.audioBuffer,
            f.file.name.replace(/\.[0-9a-z]+$/i, ".wav")
          )
        )
      )
      waitOverlay(false)
    }
    clearButton.onclick = () => {
      this.files = []
      if (this.playing !== null) this.playPause(this.playing, false)
      this.updateUI()
    }
    sampleRateInput.onchange = bitDepthInput.onchange = channelsInput.onchange = () => {
      if (this.playing !== null) this.playPause(this.playing, false)
      this.updateUI()
    }
  }

  async add(files) {
    //do not add files with the same name twice
    const tId = setTimeout(() => waitOverlay(true), 300)
    const filesToAdd = files.filter(
      f => !this.files.map(({ file }) => file.name).includes(f.name)
    )
    this.files.push(
      ...(await Promise.all(
        filesToAdd.map(async file => ({
          file,
          audioBuffer: await new AudioContext().decodeAudioData(
            await file.arrayBuffer()
          )
        }))
      ))
    )
    this.files.sort((a, b) => a.file.name.localeCompare(b.file.name))
    clearTimeout(tId)
    waitOverlay(false)
    this.updateUI()
  }
  remove(index) {
    if (this.playing !== null) this.playPause(this.playing, false)
    this.files.splice(index, 1)
    this.updateUI()
  }
  playPause(index, updateUI = true) {
    if (this.playing === index) {
      if (this.stopPlaying) {
        this.stopPlaying()
        this.stopPlaying = null
        this.playing = null
      }
    } else {
      if (this.playing !== null) this.playPause(this.playing, false)
      this.playing = index
      this.playAudioBuffer(this.files[index].audioBuffer)
    }
    if (updateUI) this.updateUI()
  }

  async playAudioBuffer(audioBufferIn) {
    const targetOptions = this.getTargetOptions()
    const audioCtx = new AudioContext()
    const audioBuffer = await processAudioFile(
      audioBufferIn,
      targetOptions.channelOpt,
      targetOptions.sampleRate
    )
    const song = audioCtx.createBufferSource()
    song.buffer = audioBuffer
    song.connect(audioCtx.destination)
    song.start()
    this.stopPlaying = () => song.stop()
    song.onended = () => this.playing !== null && this.playPause(this.playing)
  }

  async convertAndSaveAudioBuffer(audioBufferIn, saveFileName) {
    const targetOptions = this.getTargetOptions()
    const audioBuffer = await processAudioFile(
      audioBufferIn,
      targetOptions.channelOpt,
      targetOptions.sampleRate
    )
    const rawData = audioToRawWave(
      targetOptions.channelOpt === "both"
        ? [audioBuffer.getChannelData(0), audioBuffer.getChannelData(1)]
        : [audioBuffer.getChannelData(0)],
      targetOptions.bytesPerSample
    )
    const blob = makeWav(
      rawData,
      targetOptions.channelOpt === "both" ? 2 : 1,
      targetOptions.sampleRate,
      targetOptions.bytesPerSample
    )

    saveAs(blob, saveFileName)
  }

  async updateUI() {
    const targetOptions = this.getTargetOptions()
    fileTableBodyElem.innerHTML = makeFileTableRows(
      this.files.map(({ file }) => file),
      this.playing,
      this.files.map(({ audioBuffer, file }) => ({
        duration: audioBuffer.duration,
        inSize: file.size,
        outSize:
          (audioBuffer.length / audioBuffer.sampleRate) *
          targetOptions.sampleRate *
          targetOptions.bytesPerSample *
          (targetOptions.channelOpt === "both" ? 2 : 1)
      }))
    )
    clearButton.disabled = saveButton.disabled = !this.files.length
  }

  getTargetOptions() {
    return {
      sampleRate: Math.round(Number(sampleRateInput.value)),
      bytesPerSample: Math.round(Number(bitDepthInput.value)) === 8 ? 1 : 2,
      channelOpt: channelsInput.value
    }
  }
}

const audioFilesProcessor = new AudioFilesProcessor()

initOpenFiles(files => {
  const audioFiles = files.filter(f => f.type.startsWith("audio/"))
  if (!audioFiles.length) return
  audioFilesProcessor.add(audioFiles)
})

const saveAs = (blob, fileName) => {
  var a = document.createElement("a")
  document.body.appendChild(a)
  a.style.display = "none"
  const url = window.URL.createObjectURL(blob)
  a.href = url
  a.download = fileName
  a.click()
  setTimeout(() => window.URL.revokeObjectURL(url), 1000)
}

/* --- Audio processing --- */

const audioResample = (buffer, sampleRate) => {
  const offlineCtx = new OfflineAudioContext(
    2,
    (buffer.length / buffer.sampleRate) * sampleRate,
    sampleRate
  )
  const source = offlineCtx.createBufferSource()
  source.buffer = buffer
  source.connect(offlineCtx.destination)
  source.start()
  return offlineCtx.startRendering()
}

const audioReduceChannels = (buffer, targetChannelOpt) => {
  if (targetChannelOpt === "both" || buffer.numberOfChannels < 2) return buffer
  const outBuffer = new AudioBuffer({
    sampleRate: buffer.sampleRate,
    length: buffer.length,
    numberOfChannels: 1
  })

  const data = [buffer.getChannelData(0), buffer.getChannelData(1)]
  const newData = new Float32Array(buffer.length)
  for (let i = 0; i < buffer.length; ++i)
    newData[i] =
      targetChannelOpt === "left"
        ? data[0][i]
        : targetChannelOpt === "right"
        ? data[1][i]
        : (data[0][i] + data[1][i]) / 2
  outBuffer.copyToChannel(newData, 0)
  return outBuffer
}

const audioNormalize = buffer => {
  const data = Array.from(Array(buffer.numberOfChannels)).map((_, idx) =>
    buffer.getChannelData(idx)
  )
  const maxAmplitude = Math.max(
    ...data.map(chan =>
      chan.reduce((acc, cur) => Math.max(acc, Math.abs(cur)), 0)
    )
  )
  if (maxAmplitude >= 1.0) return buffer
  const coeff = 1.0 / maxAmplitude
  data.forEach(chan => {
    chan.forEach((v, idx) => (chan[idx] = v * coeff))
    buffer.copyToChannel(chan, 0)
  })
  return buffer
}

const processAudioFile = async (
  audioBufferIn,
  targetChannelOpt,
  targetSampleRate
) => {
  const resampled = await audioResample(audioBufferIn, targetSampleRate)
  const reduced = audioReduceChannels(resampled, targetChannelOpt)
  const normalized = audioNormalize(reduced)
  return normalized
}

const audioToRawWave = (audioChannels, bytesPerSample, mixChannels = false) => {
  const bufferLength = audioChannels[0].length
  const numberOfChannels = audioChannels.length === 1 ? 1 : 2
  const reducedData = new Uint8Array(
    bufferLength * numberOfChannels * bytesPerSample
  )
  for (let i = 0; i < bufferLength; ++i) {
    for (
      let channel = 0;
      channel < (mixChannels ? 1 : numberOfChannels);
      ++channel
    ) {
      const outputIndex = (i * numberOfChannels + channel) * bytesPerSample
      let sample
      if (!mixChannels) sample = audioChannels[channel][i]
      else
        sample =
          audioChannels.reduce((prv, cur) => prv + cur[i], 0) / numberOfChannels
      sample = sample > 1 ? 1 : sample < -1 ? -1 : sample //check for clipping
      //bit reduce and convert to Uint8
      switch (bytesPerSample) {
        case 2:
          sample = sample * 32767
          reducedData[outputIndex] = sample
          reducedData[outputIndex + 1] = sample >> 8
          break
        case 1:
          reducedData[outputIndex] = (sample + 1) * 127
          break
        default:
          throw "Only 8, 16 bits per sample are supported"
      }
    }
  }
  return reducedData
}

const makeWav = (data, channels, sampleRate, bytesPerSample) => {
  const headerLength = 44
  var wav = new Uint8Array(headerLength + data.length)
  var view = new DataView(wav.buffer)

  view.setUint32(0, 1380533830, false) // RIFF identifier 'RIFF'
  view.setUint32(4, 36 + data.length, true) // file length minus RIFF identifier length and file description length
  view.setUint32(8, 1463899717, false) // RIFF type 'WAVE'
  view.setUint32(12, 1718449184, false) // format chunk identifier 'fmt '
  view.setUint32(16, 16, true) // format chunk length
  view.setUint16(20, 1, true) // sample format (raw)
  view.setUint16(22, channels, true) // channel count
  view.setUint32(24, sampleRate, true) // sample rate
  view.setUint32(28, sampleRate * bytesPerSample * channels, true) // byte rate (sample rate * block align)
  view.setUint16(32, bytesPerSample * channels, true) // block align (channel count * bytes per sample)
  view.setUint16(34, bytesPerSample * 8, true) // bits per sample
  view.setUint32(36, 1684108385, false) // data chunk identifier 'data'
  view.setUint32(40, data.length, true) // data chunk length

  wav.set(data, headerLength)

  return new Blob([wav.buffer], { type: "audio/wav" })
}

/* --- --- */
