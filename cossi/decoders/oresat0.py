# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Oresat0(KaitaiStruct):
    """:field name: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    
    Attention: `rpt_callsign` cannot be accessed because `rpt_instance` is an
    array of unknown size at the beginning of the parsing process! Left an
    example in here.
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Oresat0.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Oresat0.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = Oresat0.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = Oresat0.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = Oresat0.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = Oresat0.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = Oresat0.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = Oresat0.IFrame(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Oresat0.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Oresat0.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Oresat0.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Oresat0.SsidMask(self._io, self, self._root)
            if (self.src_ssid_raw.ssid_mask & 1) == 0:
                self.repeater = Oresat0.Repeater(self._io, self, self._root)

            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Oresat0.Ax25InfoData(_io__raw_ax25_info, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Oresat0.Ax25InfoData(_io__raw_ax25_info, self, self._root)


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return self._m_ssid if hasattr(self, '_m_ssid') else None


    class Repeaters(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_callsign_raw = Oresat0.CallsignRaw(self._io, self, self._root)
            self.rpt_ssid_raw = Oresat0.SsidMask(self._io, self, self._root)


    class Repeater(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_instance = []
            i = 0
            while True:
                _ = Oresat0.Repeaters(self._io, self, self._root)
                self.rpt_instance.append(_)
                if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                    break
                i += 1


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = Oresat0.Callsign(_io__raw_callsign_ror, self, self._root)


    class Ax25InfoData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.aprs_packet_data_type_identifier = self._io.read_u1()
            self.aprs_packet_revision = self._io.read_u1()
            self.c3_m4_oresat0_state = self._io.read_bits_int_be(1) != 0
            self._io.align_to_byte()
            self.c3_m4_uptime = self._io.read_u4le()
            self.c3_rtc_time = self._io.read_u4le()
            self.c3_m4_temperature = self._io.read_s1()
            self.c3_m4_ref_voltage = self._io.read_u1()
            self.c3_m4_vbusp_voltage = self._io.read_u1()
            self.c3_m4_vbusp_current = self._io.read_u1()
            self.c3_wdt_num_timeouts = self._io.read_u2le()
            self.c3_emmc_perc_full = self._io.read_u1()
            self.c3_l_rx_bytes_received = self._io.read_u4le()
            self.c3_l_rx_valid_packets = self._io.read_u4le()
            self.c3_l_rx_rssi = self._io.read_u1()
            self.c3_l_rx_pll_lock = self._io.read_bits_int_be(1) != 0
            self._io.align_to_byte()
            self.c3_uhf_tx_temperature = self._io.read_s1()
            self.c3_uhf_tx_fwd_forward_power = self._io.read_u2le()
            self.c3_uhf_tx_rev_reverse_power = self._io.read_u2le()
            self.c3_uhf_rx_bytes_received = self._io.read_u4le()
            self.c3_uhf_rx_valid_packets = self._io.read_u4le()
            self.c3_uhf_rx_rssi = self._io.read_u1()
            self.c3_uhf_rx_pll_lock = self._io.read_bits_int_be(1) != 0
            self.c3_deployer_1_read_back = self._io.read_bits_int_be(1) != 0
            self.c3_can1_state = self._io.read_bits_int_be(1) != 0
            self.c3_can2_state = self._io.read_bits_int_be(1) != 0
            self._io.align_to_byte()
            self.c3_opd_current = self._io.read_u1()
            self.c3_opd_state = self._io.read_u1()
            self.battery_pack_1_vbatt = self._io.read_u2le()
            self.battery_pack_1_vcell = self._io.read_u2le()
            self.battery_pack_1_vcell_max = self._io.read_u2le()
            self.battery_pack_1_vcell_min = self._io.read_u2le()
            self.battery_pack_1_vcell_1 = self._io.read_u2le()
            self.battery_pack_1_vcell_2 = self._io.read_u2le()
            self.battery_pack_1_vcell_avg = self._io.read_u2le()
            self.battery_pack_1_temperature = self._io.read_s2le()
            self.battery_pack_1_temperature_avg = self._io.read_s2le()
            self.battery_pack_1_temperature_max = self._io.read_s2le()
            self.battery_pack_1_temperature_min = self._io.read_s2le()
            self.battery_pack_1_current = self._io.read_s2le()
            self.battery_pack_1_current_avg = self._io.read_s2le()
            self.battery_pack_1_current_max = self._io.read_s2le()
            self.battery_pack_1_current_min = self._io.read_s2le()
            self.battery_pack_1_state = self._io.read_u1()
            self.battery_pack_1_reported_state_of_charge = self._io.read_u1()
            self.battery_pack_1_full_capacity = self._io.read_u2le()
            self.battery_pack_1_reported_capacity = self._io.read_u2le()
            self.battery_pack_2_vbatt = self._io.read_u2le()
            self.battery_pack_2_vcell = self._io.read_u2le()
            self.battery_pack_2_vcell_max = self._io.read_u2le()
            self.battery_pack_2_vcell_min = self._io.read_u2le()
            self.battery_pack_2_vcell_1 = self._io.read_u2le()
            self.battery_pack_2_vcell_2 = self._io.read_u2le()
            self.battery_pack_2_vcell_avg = self._io.read_u2le()
            self.battery_pack_2_temperature = self._io.read_s2le()
            self.battery_pack_2_temperature_avg = self._io.read_s2le()
            self.battery_pack_2_temperature_max = self._io.read_s2le()
            self.battery_pack_2_temperature_min = self._io.read_s2le()
            self.battery_pack_2_current = self._io.read_s2le()
            self.battery_pack_2_current_avg = self._io.read_s2le()
            self.battery_pack_2_current_max = self._io.read_s2le()
            self.battery_pack_2_current_min = self._io.read_s2le()
            self.battery_pack_2_state = self._io.read_u1()
            self.battery_pack_2_reported_state_of_changed = self._io.read_u1()
            self.battery_pack_2_full_capacity = self._io.read_u2le()
            self.battery_pack_2_reported_capacity = self._io.read_u2le()
            self.solar_minus_x_voltage_avg = self._io.read_u2le()
            self.solar_minus_x_current_avg = self._io.read_s2le()
            self.solar_minus_x_power_avg = self._io.read_u2le()
            self.solar_minus_x_voltage_max = self._io.read_u2le()
            self.solar_minus_x_current_max = self._io.read_s2le()
            self.solar_minus_x_power_max = self._io.read_u2le()
            self.solar_minus_x_energy = self._io.read_u2le()
            self.solar_minus_y_voltage_avg = self._io.read_u2le()
            self.solar_minus_y_current_avg = self._io.read_s2le()
            self.solar_minus_y_power_avg = self._io.read_u2le()
            self.solar_minus_y_voltage_max = self._io.read_u2le()
            self.solar_minus_y_current_max = self._io.read_s2le()
            self.solar_minus_y_power_max = self._io.read_u2le()
            self.solar_minus_y_energy = self._io.read_u2le()
            self.solar_plus_x_voltage_avg = self._io.read_u2le()
            self.solar_plus_x_current_avg = self._io.read_s2le()
            self.solar_plus_x_power_avg = self._io.read_u2le()
            self.solar_plus_x_voltage_max = self._io.read_u2le()
            self.solar_plus_x_current_max = self._io.read_s2le()
            self.solar_plus_x_power_max = self._io.read_u2le()
            self.solar_plus_x_energy = self._io.read_u2le()
            self.solar_plus_y_voltage_avg = self._io.read_u2le()
            self.solar_plus_y_current_avg = self._io.read_s2le()
            self.solar_plus_y_power_avg = self._io.read_u2le()
            self.solar_plus_y_voltage_max = self._io.read_u2le()
            self.solar_plus_y_current_max = self._io.read_s2le()
            self.solar_plus_y_power_max = self._io.read_u2le()
            self.solar_plus_y_energy = self._io.read_u2le()
            self.star_tracker_emmc_capacity = self._io.read_u1()
            self.star_tracker_readable_files = self._io.read_u1()
            self.star_tracker_updater_status = self._io.read_u1()
            self.star_tracker_updates_cached = self._io.read_u1()
            self.star_tracker_right_ascension = self._io.read_s2le()
            self.star_tracker_declination = self._io.read_s2le()
            self.star_tracker_roll = self._io.read_s2le()
            self.star_tracker_timestamp_of_last_packet = self._io.read_u4le()
            self.gps_emmc_capacity = self._io.read_u1()
            self.gps_readable_files = self._io.read_u1()
            self.gps_updater_status = self._io.read_u1()
            self.gps_updates_cached = self._io.read_u1()
            self.gps_gps_status = self._io.read_u1()
            self.gps_num_of_sats_locked = self._io.read_u1()
            self.gps_x_position = self._io.read_s4le()
            self.gps_y_postition = self._io.read_s4le()
            self.gps_z_position = self._io.read_s4le()
            self.gps_x_velocity = self._io.read_s4le()
            self.gps_y_velocity = self._io.read_s4le()
            self.gps_z_velocity = self._io.read_s4le()
            self.gps_timestamp_of_last_packet = self._io.read_u4le()
            self.ads_gyro_roll_dot = self._io.read_s2le()
            self.ads_gyro_pitch_dot = self._io.read_s2le()
            self.ads_gyro_yaw_dot = self._io.read_s2le()
            self.ads_gyro_imu_temp = self._io.read_s1()
            self.dxwifi_emmc_capacity = self._io.read_u1()
            self.dxwifi_readable_files = self._io.read_u1()
            self.dxwifi_updater_status = self._io.read_u1()
            self.dxwifi_updates_cached = self._io.read_u1()
            self.dxwifi_transmitting = self._io.read_bits_int_be(1) != 0
            self._io.align_to_byte()
            self.aprs_packet_crc_minus_32 = self._io.read_u4le()



