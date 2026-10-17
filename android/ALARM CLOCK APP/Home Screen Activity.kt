class HomeActivity : AppCompatActivity() {
    private lateinit var currentTimeTextView: TextView
    private lateinit var setAlarmButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        currentTimeTextView = findViewById(R.id.currentTimeTextView)
        setAlarmButton = findViewById(R.id.setAlarmButton)

        // Update current time every second
        val handler = Handler(Looper.getMainLooper())
        handler.post(object : Runnable {
            override fun run() {
                val currentTime = SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date())
                currentTimeTextView.text = currentTime
                handler.postDelayed(this, 1000)
            }
        })

        setAlarmButton.setOnClickListener {
            // Navigate to Alarm Setting Activity
            startActivity(Intent(this, AlarmSettingActivity::class.java))
        }
    }
}