package com.example.mallesh.sensor_record;

import com.payfone.sdk.*;

import android.app.AlertDialog;
import android.provider.Settings;
import android.app.ListActivity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;

import org.influxdb.BatchOptions;
import org.influxdb.InfluxDB;
import org.influxdb.InfluxDBFactory;
import org.influxdb.dto.Point;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.Timer;
import java.util.TimerTask;

import javax.net.ssl.*;

import okhttp3.OkHttpClient;

public class MainActivity extends ListActivity implements SensorEventListener {
    //global variables
    public SensorEventListener mSensorListener;
    public SensorManager sensorManager;
    public List<Sensor> listSensor;
    private Sensor mAccelerometer, mGyroscope;
    private static float acc_x = -1;
    private static float acc_y = -1;
    private static float acc_z = -1;
    private static float gyro_x = -1;
    private static float gyro_y = -1;
    private static float gyro_z = -1;

    private final static String INFLUX_HOST = "https://influx-cewit.netsmartdev.com:443";
    private static String INFLUX_DATABASE = "db_team_69";
    private static String INFLUX_USER = "user_team_69";
    private static String INFLUX_PASS = "J9sdscUlGImEzBEP";

    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //retrieving the list of sensors available on a device
        sensorManager
                = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        listSensor
                = sensorManager.getSensorList(Sensor.TYPE_ALL);
        mAccelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        mGyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);

        int reporting_period_ms = 10;
        Timer _t = new Timer();
        _t.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                //System.out.println("Sending Data Points");
                try {
                    //insertDataPoints(INFLUX_DATABASE, INFLUX_USER, INFLUX_PASS);
                } catch (Exception e) {
                    System.out.println("Caught something");
                }
            }
        }, 0, reporting_period_ms);


        /// [Options Example]
        PayfoneOptions payfoneOptions = new PayfoneOptions() {
        /*
            The required override: You need to provide the Payfone SDK with
            the Activity that will be active while the authentication is taking
            place.
         */
        @Override
        public MainActivity getActivity() {
            return MainActivity.this;
        }

        /*
            Optional override.

            If you want to handle specific failure modes in a custom manner,
            this is the place to add such code. Otherwise you can leave the
            default handler in place.
         */
        @Override
        public void handleFailure(final PayfoneOptions.FailureMode failureMode, String message) {
            AlertDialog.Builder alert = new
                    AlertDialog.Builder(MainActivity.this);
            alert.setTitle("Authentication Failed");
            alert.setMessage(message);
            alert.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int whichButton) {
                    if (failureMode == FailureMode.WIFI_CALLING_ENABLED) {
                        startActivity(new
                                Intent(Settings.ACTION_WIFI_SETTINGS));
                    } // else do nothing
                }
            });

            alert.show();
            System.out.println(message);
        }

        /*
            An optional override that you can supply that will notify you when
            the device cellular IP is available. It will call your code in the
            UI thread, so it's safe to use the result to set a UI field, as in
            the example below.

            It's safe to delete this override if you don't need it.
         */
        @Override
        public void identifiedCellularIP(final String deviceCellularIP) {
            System.out.println("Found IP Address:" + deviceCellularIP);
        }
        };
        payfoneOptions.mDebugMode = 1;
        // Create the PayfoneSDK using the options set above.
        PayfoneSDK mPayfoneSDK = new PayfoneSDK(payfoneOptions);

        Thread thread = new Thread(new Runnable() {

            @Override
            public void run() {

                    System.out.println("Payphone stuff");
                try {
                        // If this call fails, it will also trigger a call to
                        // the handleFailure() override.
                        if (!mPayfoneSDK.isAuthenticationPossible()) {
                            System.out.println("Not possibleeeeeee!");
                        } else {
                            System.out.println("Possibleeeeeee!");
                            //System.out.println(mPayfoneSDK.isAuthenticationPossible());
                        }
                } catch (Exception e) {
                    System.out.println("Caught");
                }
            }
        });

        thread.start();



    }

    protected void onResume() {
        super.onResume();
        sensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        sensorManager.registerListener(this, mGyroscope, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    protected void onPause() {
        sensorManager.unregisterListener(mSensorListener);
        super.onPause();

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // TODO Auto-generated method stub

    }

    private static void insertDataPoints(String database, String user, String password) throws InterruptedException {

        try {
            final TrustManager[] trustAllCerts = new TrustManager[]{
                    new X509TrustManager() {
                        @Override
                        public void checkClientTrusted(java.security.cert.X509Certificate[] chain, String authType) {
                        }

                        @Override
                        public void checkServerTrusted(java.security.cert.X509Certificate[] chain, String authType) {
                        }

                        @Override
                        public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                            return new java.security.cert.X509Certificate[]{};
                        }
                    }
            };

            // Install the all-trusting trust manager
            final SSLContext sslContext = SSLContext.getInstance("SSL");
            sslContext.init(null, trustAllCerts, new java.security.SecureRandom());
            // Create an ssl socket factory with our all-trusting manager
            final SSLSocketFactory sslSocketFactory = sslContext.getSocketFactory();

            OkHttpClient.Builder builder = new OkHttpClient.Builder();
            builder.sslSocketFactory(sslSocketFactory, (X509TrustManager) trustAllCerts[0]);
            builder.hostnameVerifier(new HostnameVerifier() {
                @Override
                public boolean verify(String hostname, SSLSession session) {
                    return true;
                }
            });
//        OkHttpClient.Builder builder = new OkHttpClient.Builder();
//        builder.hostnameVerifier(new HostnameVerifier() {
//            @Override
//            public boolean verify(String hostname, SSLSession session) {
//                return true;
//            }
//        });
            try (InfluxDB influxDB = InfluxDBFactory.connect(INFLUX_HOST, user, password, builder)) {

                // Set up exception handler
                influxDB.enableBatch(BatchOptions.DEFAULTS.exceptionHandler(
                        (failedPoints, throwable) -> {
                            for (Point failedPoint : failedPoints) {
                                System.err.println("[ERROR] Failed Point: " + failedPoint);
                            }
                            System.err.println(throwable);
                        })
                );

                // Set Database
                influxDB.setDatabase(database);

                // Create tags
                Map<String, String> tags = new HashMap<>();
                //            tags.put("component", "primary_web_app");
                //            tags.put("type", "method_timer");

                // Send 10 random metric values into the database

                // Random response time
                //                int responseTime = ThreadLocalRandom.current().nextInt(50, 10000);
                //
                //                // Random request size
                //                int payloadSize = ThreadLocalRandom.current().nextInt(1024, 10000);

                System.out.println("Before Sending");
                System.out.println(acc_x);
                System.out.println(acc_y);
                System.out.println(acc_z);

                // Create Point
                Point point = Point.measurement("fake_sensor_data")
                        .time(System.currentTimeMillis(), TimeUnit.MILLISECONDS)
                        .tag(tags)
                        .addField("fake_acc_x", acc_x)
                        .addField("fake_acc_y", acc_y)
                        .addField("fake_acc_z", acc_z)
                        .addField("fake_gyro_x", gyro_x)
                        .addField("fake_gyro_y", gyro_y)
                        .addField("fake_gyro_z", gyro_z)
                        .build();

                // Write Point
                influxDB.write(point);
                System.out.println("[info] Wrote Point to Influx Db @ " + INFLUX_HOST + "/" + INFLUX_DATABASE);
            }
        } catch (Exception e) {
            System.out.println("Something caught");
        }
    }

    @Override
    public final void onSensorChanged(SensorEvent event) {
        String sensor_name = event.sensor.getName();
        //System.out.println("event.sensor.getName():" + sensor_name);

        switch (sensor_name) {
            case "LSM6DSM Accelerometer":
                acc_x = event.values[0];
                acc_y = event.values[1];
                acc_z = event.values[2];
                break;
            case "LSM6DSM Gyroscope":
                gyro_x = event.values[0];
                gyro_y = event.values[1];
                gyro_z = event.values[2];
                break;
        }
//        System.out.println(event.values[0]);
//        System.out.println(event.values[1]);
//        System.out.println(event.values[2]);
//        System.out.println(acc_x);
//        System.out.println(acc_y);
//        System.out.println(acc_z);
    }



}