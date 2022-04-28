export const beautifyName = (name) => {
    var beautifulName = name.replace('_', ' ').replace('  ', ' ')
    if (beautifulName.startsWith('q')) {
        beautifulName = `${ beautifulName.substring(1) } Qualitative` 
    }
    return beautifulName
}

export const pluginChartBackground = {
    id: 'white_background',
    beforeDraw: (chart) => {
        const ctx = chart.canvas.getContext('2d')
        ctx.save()
        ctx.globalCompositeOperation = 'destination-over'
        ctx.fillStyle = 'white'
        ctx.fillRect(0, 0, chart.width, chart.height)
        ctx.restore()
    }
}